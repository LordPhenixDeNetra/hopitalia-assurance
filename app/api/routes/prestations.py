from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.prestation import Prestation
from app.schemas.prestation import (
    PrestationCreate,
    PrestationRead,
    PrestationExcel,
    PrestationUpdate,
    PrestationPage,
    PrestationImportResponse,
)


router = APIRouter(prefix="/prestations", tags=["prestations"])


def _to_model(c: PrestationCreate) -> Prestation:
    return Prestation(
        order_number=c.order_number,
        date=c.date,
        last_name=c.last_name,
        first_name=c.first_name,
        invoice_number=c.invoice_number,
        patient_index=c.patient_index,
        matricule=c.matricule,
        specialty=c.specialty,
        act=c.act,
        rate_percent=Decimal(str(c.rate_percent)),
        patient_share=Decimal(str(c.patient_share)),
        employee_share=Decimal(str(c.employee_share)),
        total_amount=Decimal(str(c.total_amount)),
        adjustment=Decimal(str(c.adjustment)),
    )


@router.get("/", response_model=List[PrestationRead])
def list_prestations(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    invoice_number: Optional[str] = None,
    matricule: Optional[str] = None,
    specialty: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    stmt = select(Prestation)
    conditions = []
    if invoice_number:
        conditions.append(Prestation.invoice_number == invoice_number)
    if matricule:
        conditions.append(Prestation.matricule == matricule)
    if specialty:
        conditions.append(Prestation.specialty == specialty)
    if date_from:
        from datetime import date
        try:
            df = date.fromisoformat(date_from)
            conditions.append(Prestation.date >= df)
        except Exception:
            pass
    if date_to:
        from datetime import date
        try:
            dt = date.fromisoformat(date_to)
            conditions.append(Prestation.date <= dt)
        except Exception:
            pass
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.offset(skip).limit(limit)
    rows = db.execute(stmt).scalars().all()
    return [PrestationRead.model_validate(r, from_attributes=True) for r in rows]


@router.get("/page", response_model=PrestationPage)
def list_prestations_page(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    invoice_number: Optional[str] = None,
    matricule: Optional[str] = None,
    specialty: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    stmt = select(Prestation)
    count_stmt = select(func.count()).select_from(Prestation)
    conditions = []
    if invoice_number:
        conditions.append(Prestation.invoice_number == invoice_number)
    if matricule:
        conditions.append(Prestation.matricule == matricule)
    if specialty:
        conditions.append(Prestation.specialty == specialty)
    if date_from:
        from datetime import date
        try:
            df = date.fromisoformat(date_from)
            conditions.append(Prestation.date >= df)
        except Exception:
            pass
    if date_to:
        from datetime import date
        try:
            dt = date.fromisoformat(date_to)
            conditions.append(Prestation.date <= dt)
        except Exception:
            pass
    if conditions:
        stmt = stmt.where(and_(*conditions))
        count_stmt = count_stmt.where(and_(*conditions))

    stmt = stmt.offset(skip).limit(limit)
    rows = db.execute(stmt).scalars().all()
    total = db.execute(count_stmt).scalar_one()

    return PrestationPage(
        items=[PrestationRead.model_validate(r, from_attributes=True) for r in rows],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{prestation_id}", response_model=PrestationRead)
def get_prestation(prestation_id: int, db: Session = Depends(get_db)):
    obj = db.get(Prestation, prestation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Prestation non trouvée")
    return PrestationRead.model_validate(obj, from_attributes=True)


@router.post("/", response_model=PrestationRead, status_code=201)
def create_prestation(payload: PrestationCreate, db: Session = Depends(get_db)):
    obj = _to_model(payload)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return PrestationRead.model_validate(obj, from_attributes=True)


def _apply_update(obj: Prestation, payload: PrestationUpdate) -> None:
    for field, value in payload.model_dump(exclude_unset=True).items():
        if field in {"rate_percent", "patient_share", "employee_share", "total_amount", "adjustment"} and value is not None:
            setattr(obj, field, Decimal(str(value)))
        else:
            setattr(obj, field, value)


@router.put("/{prestation_id}", response_model=PrestationRead)
def update_prestation_full(prestation_id: int, payload: PrestationCreate, db: Session = Depends(get_db)):
    obj = db.get(Prestation, prestation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Prestation non trouvée")
    # Overwrite all fields via conversion
    updated = _to_model(payload)
    obj.order_number = updated.order_number
    obj.date = updated.date
    obj.last_name = updated.last_name
    obj.first_name = updated.first_name
    obj.invoice_number = updated.invoice_number
    obj.patient_index = updated.patient_index
    obj.matricule = updated.matricule
    obj.specialty = updated.specialty
    obj.act = updated.act
    obj.rate_percent = updated.rate_percent
    obj.patient_share = updated.patient_share
    obj.employee_share = updated.employee_share
    obj.total_amount = updated.total_amount
    obj.adjustment = updated.adjustment
    db.commit()
    db.refresh(obj)
    return PrestationRead.model_validate(obj, from_attributes=True)


@router.patch("/{prestation_id}", response_model=PrestationRead)
def update_prestation_partial(prestation_id: int, payload: PrestationUpdate, db: Session = Depends(get_db)):
    obj = db.get(Prestation, prestation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Prestation non trouvée")
    _apply_update(obj, payload)
    db.commit()
    db.refresh(obj)
    return PrestationRead.model_validate(obj, from_attributes=True)


@router.delete("/{prestation_id}", status_code=204)
def delete_prestation(prestation_id: int, db: Session = Depends(get_db)):
    obj = db.get(Prestation, prestation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Prestation non trouvée")
    db.delete(obj)
    db.commit()
    return None


@router.post(
    "/import",
    summary="Importer des prestations depuis un fichier Excel (.xls)",
    response_model=PrestationImportResponse,
)
async def import_prestations(file: UploadFile, db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".xls"):
        raise HTTPException(status_code=400, detail="Veuillez fournir un fichier .xls")

    try:
        import xlrd
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="xlrd n'est pas installé. Ajoutez 'xlrd' dans requirements et installez les dépendances.",
        )

    data = await file.read()
    try:
        wb = xlrd.open_workbook(file_contents=data)
    except Exception:
        raise HTTPException(status_code=400, detail="Impossible de lire le fichier .xls")

    sheet = wb.sheet_by_index(0)
    headers = [str(sheet.cell_value(0, c)).strip() for c in range(sheet.ncols)]
    created = 0

    try:
        for r in range(1, sheet.nrows):
            row_vals = [sheet.cell_value(r, c) for c in range(sheet.ncols)]
            excel_item = PrestationExcel.from_excel_row(headers, row_vals, wb.datemode)
            model_item = _to_model(PrestationCreate(**excel_item.model_dump()))
            db.add(model_item)
            created += 1
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur d'import: {e}")

    return PrestationImportResponse(created=created)


@router.get("/export", summary="Exporter les prestations filtrées en CSV")
def export_prestations_csv(
    db: Session = Depends(get_db),
    invoice_number: Optional[str] = None,
    matricule: Optional[str] = None,
    specialty: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    stmt = select(Prestation)
    conditions = []
    if invoice_number:
        conditions.append(Prestation.invoice_number == invoice_number)
    if matricule:
        conditions.append(Prestation.matricule == matricule)
    if specialty:
        conditions.append(Prestation.specialty == specialty)
    if date_from:
        from datetime import date
        try:
            df = date.fromisoformat(date_from)
            conditions.append(Prestation.date >= df)
        except Exception:
            pass
    if date_to:
        from datetime import date
        try:
            dt = date.fromisoformat(date_to)
            conditions.append(Prestation.date <= dt)
        except Exception:
            pass
    if conditions:
        stmt = stmt.where(and_(*conditions))

    rows = db.execute(stmt).scalars().all()

    import io, csv

    output = io.StringIO()
    writer = csv.writer(output)
    headers = [
        "id",
        "order_number",
        "date",
        "last_name",
        "first_name",
        "invoice_number",
        "patient_index",
        "matricule",
        "specialty",
        "act",
        "rate_percent",
        "patient_share",
        "employee_share",
        "total_amount",
        "adjustment",
    ]
    writer.writerow(headers)

    def fmt_decimal(d):
        return (str(d) if d is not None else "")

    for r in rows:
        writer.writerow([
            r.id,
            r.order_number if r.order_number is not None else "",
            r.date.isoformat(),
            r.last_name,
            r.first_name,
            r.invoice_number,
            r.patient_index,
            r.matricule,
            r.specialty,
            r.act,
            fmt_decimal(r.rate_percent),
            fmt_decimal(r.patient_share),
            fmt_decimal(r.employee_share),
            fmt_decimal(r.total_amount),
            fmt_decimal(r.adjustment),
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": "attachment; filename=prestations.csv",
        },
    )