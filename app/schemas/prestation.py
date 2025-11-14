from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class PrestationBase(BaseModel):
    order_number: Optional[int] = None
    date: date
    last_name: str
    first_name: str
    invoice_number: str
    patient_index: str
    matricule: str
    specialty: str
    act: str
    rate_percent: float
    patient_share: float
    employee_share: float
    total_amount: float
    adjustment: float

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )


class PrestationCreate(PrestationBase):
    pass


class PrestationRead(PrestationBase):
    id: int


class PrestationUpdate(BaseModel):
    order_number: Optional[int] = None
    date: Optional[date] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    invoice_number: Optional[str] = None
    patient_index: Optional[str] = None
    matricule: Optional[str] = None
    specialty: Optional[str] = None
    act: Optional[str] = None
    rate_percent: Optional[float] = None
    patient_share: Optional[float] = None
    employee_share: Optional[float] = None
    total_amount: Optional[float] = None
    adjustment: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )


class PrestationPage(BaseModel):
    items: List[PrestationRead]
    total: int
    skip: int
    limit: int


class PrestationImportResponse(BaseModel):
    created: int


class PrestationExcel(BaseModel):
    order_number: Optional[int] = None
    date: date
    last_name: str
    first_name: str
    invoice_number: str
    patient_index: str
    matricule: str
    specialty: str
    act: str
    rate_percent: float
    patient_share: float
    employee_share: float
    total_amount: float
    adjustment: float

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    @classmethod
    def header_aliases(cls) -> Dict[str, str]:
        return {
            "N° d'ordre": "order_number",
            "Date": "date",
            "Nom": "last_name",
            "Prenom": "first_name",
            "N° Facture": "invoice_number",
            "Index Patient": "patient_index",
            "Matricule": "matricule",
            "Spécialité": "specialty",
            "Acte": "act",
            "Taux": "rate_percent",
            "Part Patient": "patient_share",
            "Part Employé": "employee_share",
            "Montant Total": "total_amount",
            "Reglage": "adjustment",
        }

    @classmethod
    def from_excel_row(
        cls, headers: List[str], values: List[Any], datemode: int
    ) -> "PrestationExcel":
        mapping = cls.header_aliases()
        data: Dict[str, Any] = {}
        for idx, h in enumerate(headers):
            key = mapping.get(h)
            if not key:
                continue
            val = values[idx]

            if key == "order_number":
                try:
                    data[key] = int(val) if val not in (None, "") else None
                except Exception:
                    data[key] = None

            elif key == "date":
                if isinstance(val, (int, float)):
                    try:
                        import xlrd

                        dt = xlrd.xldate_as_datetime(val, datemode)
                        data[key] = dt.date()
                    except Exception:
                        data[key] = date(1970, 1, 1)
                elif isinstance(val, str):
                    try:
                        d = datetime.strptime(val[:10], "%d/%m/%Y").date()
                        data[key] = d
                    except Exception:
                        data[key] = date(1970, 1, 1)
                else:
                    data[key] = date(1970, 1, 1)

            elif key in (
                "rate_percent",
                "patient_share",
                "employee_share",
                "total_amount",
                "adjustment",
            ):
                try:
                    data[key] = float(val) if val is not None else 0.0
                except Exception:
                    data[key] = 0.0

            else:
                data[key] = "" if val is None else str(val).strip()

        return cls(**data)