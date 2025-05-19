from fastapi import APIRouter, HTTPException, status
from src.api.dependencies import sessionDep
from src.database import engine
from src.models.DBmodels import Base, WorkersOrm, DepartmentsOrm, AttendancesOrm
from src.schemas.pydantic_schemas import WorkerDataSchema, DepartmentSchema
from sqlalchemy import delete, select


router = APIRouter()


@router.get("/")
async def check_status():
    return "connected"

@router.post("/database/create")
async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"status": "ok"}

@router.get("/worker/find/{fio}")
async def get_worker_by_fio(name: str, session: sessionDep):
    query = select(WorkersOrm).where(WorkersOrm.name == name)
    res = await session.execute(query)
    return res.scalars().all()

@router.post("/worker")
async def add_new_worker(data: WorkerDataSchema, session: sessionDep):
    new_worker = WorkersOrm(**data.model_dump())
    session.add(new_worker)
    await session.commit()

    return {"status": "ok"}

@router.put("/worker/{id}")
async def update_worker_information(data: WorkerDataSchema, id: int, session: sessionDep):
    worker = await session.get(WorkersOrm, id)
    data = data.model_dump()
    worker.name = data["name"]
    worker.adress = data["adress"]
    worker.passport_number = data["passport_number"]
    worker.passport_series = data["passport_series"]
    worker.department_id = data["department_id"]
    worker.phone_number = data["phone_number"]
    await session.commit()

    return {"status": "ok"}

@router.delete("/worker/{id}")
async def delete_worker_by_id(id: int, session: sessionDep):
    query = delete(WorkersOrm).where(WorkersOrm.id == id)
    await session.execute(query)
    await session.commit()

    return {"status": "ok"}

@router.post("/departments")
async def add_department(data: DepartmentSchema, session: sessionDep):
    new_department = DepartmentsOrm(**data.model_dump())
    session.add(new_department)
    await session.commit()

    return {"status": "ok"}

@router.put("/departments/{id}")
async def change_department_info(data: DepartmentSchema, id: int, session: sessionDep):
    data = data.model_dump()
    department = await session.get(DepartmentsOrm, id)
    department.name = data["name"]
    department.adress = data["adress"]
    await session.commit()

    return {"status": "ok"}

@router.get("/departments/all")
async def get_all_departments(session: sessionDep):
    res = await session.execute(select(DepartmentsOrm))
    return res.scalars().all()

@router.post("/attendance/{worker_id}")
async def make_attendance(worker_id: int, session: sessionDep):
    new_attend = AttendancesOrm(worker_id=worker_id)
    session.add(new_attend)
    await session.commit()

    return {"status": "ok"}

@router.get("/attendance/names")
async def show_attendance(names: str, session: sessionDep):
    qr = select(WorkersOrm).where(WorkersOrm.name.in_(names.split(";")))
    workers = await session.execute(qr)
    check = await session.execute(qr)
    workers = workers.scalars()

    if check.scalars().all():
        res = []
        for worker in workers:
            tmp = {}
            attends = worker.attend
            tmp["name"] = worker.name
            tmp["attends"] = [{"date": x.date, "time": x.time} for x in attends]
            res.append(tmp)
        return res

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/worker/names")
async def get_all_names(session: sessionDep):
    res = await session.execute(select(WorkersOrm.name))

    return res.scalars().all()

@router.get("/worker/ids")
async def get_all_ids(session: sessionDep):
    res = await session.execute(select(WorkersOrm.id))

    return res.scalars().all()