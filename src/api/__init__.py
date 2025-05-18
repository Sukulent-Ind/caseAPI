from sqlalchemy import  event
from src.database import engine
from fastapi import APIRouter


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

event.listen(engine.sync_engine, 'connect', _fk_pragma_on_connect)


from src.api.AS import router as AS_router


main_router = APIRouter()
main_router.include_router(AS_router)