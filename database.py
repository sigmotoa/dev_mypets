from sqlalchemy import Column, Float, ForeignKey, Table, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Pets(Base):
    __tablename__ = "pets"
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(20),nullable=False)
    breed: Mapped[str] = mapped_column(String(25), nullable=False)
    birth: Mapped[int] = mapped_column(Integer, nullable=False)
    kind: Mapped[str] = mapped_column(String(25), nullable=False)
    female: Mapped[bool] = mapped_column(Boolean, nullable=False)