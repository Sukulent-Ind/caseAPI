from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


engine = create_async_engine(
    url="sqlite+aiosqlite:///./sql_app.db",
    echo=True,
    pool_size=5,
    max_overflow=5
)

session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with session_factory() as session:
        yield session
