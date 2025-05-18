from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import text, ForeignKey
from typing import Annotated
import datetime


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"<<<<{self.__class__.__name__} {','.join(cols)}>>>>"


intpk = Annotated[int, mapped_column(primary_key=True)]
date = Annotated[datetime.date, mapped_column(server_default=text("date()"))]
time = Annotated[datetime.time, mapped_column(server_default=text("time()"))]


class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    name: Mapped[str]
    passport_series: Mapped[str]
    passport_number: Mapped[str]
    adress: Mapped[str]
    phone_number: Mapped[str]
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    department: Mapped["DepartmentsOrm"] = relationship(back_populates="worker", uselist=False, lazy="selectin")
    attend: Mapped[list["AttendancesOrm"]] = relationship(back_populates="worker", uselist=True, lazy="selectin")


class DepartmentsOrm(Base):
    __tablename__ = "departments"

    id: Mapped[intpk]
    name: Mapped[str]
    adress: Mapped[str]

    worker: Mapped[list["WorkersOrm"]] = relationship(back_populates="department", uselist=True)


class AttendancesOrm(Base):
    __tablename__ = "attendance"

    id: Mapped[intpk]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    date: Mapped[date]
    time: Mapped[time]

    worker: Mapped["WorkersOrm"] = relationship(back_populates="attend", uselist=False)
