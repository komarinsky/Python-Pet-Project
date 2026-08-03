from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from pet_project import models, schemas
from pet_project.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello from pet_project!"}


@app.post("/items")
def create_item(item: schemas.ItemCreate, db: DbSession) -> schemas.ItemOut:
    db_item = models.Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return schemas.ItemOut.model_validate(db_item)


@app.get("/items")
def list_items(db: DbSession) -> list[schemas.ItemOut]:
    items = db.scalars(select(models.Item)).all()
    return [schemas.ItemOut.model_validate(item) for item in items]