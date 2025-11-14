from sqlalchemy import Column, Date, Integer, Numeric, String

from app.core.database import Base


class Prestation(Base):
    __tablename__ = "prestations"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(Integer, nullable=True)
    date = Column(Date, nullable=False)

    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    invoice_number = Column(String(64), nullable=False, index=True)
    patient_index = Column(String(64), nullable=False)
    matricule = Column(String(64), nullable=False, index=True)
    specialty = Column(String(64), nullable=False)
    act = Column(String(256), nullable=False)

    rate_percent = Column(Numeric(5, 2), nullable=False)
    patient_share = Column(Numeric(12, 2), nullable=False)
    employee_share = Column(Numeric(12, 2), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    adjustment = Column(Numeric(12, 2), nullable=False)