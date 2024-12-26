import logging
from typing import Annotated
from collections.abc import Generator

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import Session, create_engine, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.configs import settings


logger = logging.getLogger("database")

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


max_tries = 1 * 5  # 5 seconds
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_db(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e

    from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    logging.info("Creating tables")
    SQLModel.metadata.create_all(engine)
