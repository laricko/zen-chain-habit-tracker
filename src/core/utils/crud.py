from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

import core.db as db_models

from .db import engine


def create(pydantic_obj: BaseModel) -> None:
    model_name = pydantic_obj.__class__.__name__
    sqlalchemy_cls = getattr(db_models, model_name)
    record = sqlalchemy_cls(**pydantic_obj.model_dump())

    with Session(engine) as session:
        session.add(record)
        session.commit()


def get_by_id(klass: type, id: UUID) -> BaseModel | None:
    sqlalchemy_cls = getattr(db_models, klass.__name__)
    with Session(engine) as session:
        record = session.get(sqlalchemy_cls, id)
        if not record:
            return
        return klass(**record.__dict__)


def get_by_kwargs(klass: type, **filters) -> list[BaseModel]:
    sqlalchemy_cls = getattr(db_models, klass.__name__)
    with Session(engine) as session:
        stmt = select(sqlalchemy_cls).filter_by(**filters)
        records = session.scalars(stmt).all()
        return [klass(**record.__dict__) for record in records]
