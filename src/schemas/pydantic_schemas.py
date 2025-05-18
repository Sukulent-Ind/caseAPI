from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class WorkerDataSchema(BaseModel):
    name: str
    passport_series: int = Field(le=9999, ge=1000)
    passport_number: int = Field(le=999999, ge=100000)
    adress: str
    phone_number: PhoneNumber
    department_id: int


class DepartmentSchema(BaseModel):
    name: str
    adress: str