from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from pet_project import crud, schemas
from pet_project.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello from pet_project!"}


# --- Shipments ---


@app.post("/shipments")
def create_shipment(shipment: schemas.ShipmentCreate, db: DbSession) -> schemas.ShipmentOut:
    db_shipment = crud.create_shipment(db, shipment)
    return schemas.ShipmentOut.model_validate(db_shipment)


@app.get("/shipments")
def list_shipments(db: DbSession) -> list[schemas.ShipmentOut]:
    shipments = crud.get_shipments(db)
    return [schemas.ShipmentOut.model_validate(s) for s in shipments]


@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: int, db: DbSession) -> schemas.ShipmentOut:
    db_shipment = crud.get_shipment(db, shipment_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return schemas.ShipmentOut.model_validate(db_shipment)


@app.put("/shipments/{shipment_id}")
def update_shipment(
    shipment_id: int, shipment: schemas.ShipmentCreate, db: DbSession
) -> schemas.ShipmentOut:
    db_shipment = crud.get_shipment(db, shipment_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    db_shipment = crud.update_shipment(db, db_shipment, shipment)
    return schemas.ShipmentOut.model_validate(db_shipment)


@app.delete("/shipments/{shipment_id}", status_code=204)
def delete_shipment(shipment_id: int, db: DbSession) -> None:
    db_shipment = crud.get_shipment(db, shipment_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    crud.delete_shipment(db, db_shipment)


# --- Items ---


@app.post("/shipments/{shipment_id}/items")
def create_item(shipment_id: int, item: schemas.ItemCreate, db: DbSession) -> schemas.ItemOut:
    db_shipment = crud.get_shipment(db, shipment_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    db_item = crud.create_item(db, item, shipment_id)
    return schemas.ItemOut.model_validate(db_item)


@app.get("/items")
def list_items(db: DbSession) -> list[schemas.ItemOut]:
    items = crud.get_items(db)
    return [schemas.ItemOut.model_validate(i) for i in items]


@app.get("/items/{item_id}")
def get_item(item_id: int, db: DbSession) -> schemas.ItemOut:
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return schemas.ItemOut.model_validate(db_item)


@app.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.ItemCreate, db: DbSession) -> schemas.ItemOut:
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = crud.update_item(db, db_item, item)
    return schemas.ItemOut.model_validate(db_item)


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: DbSession) -> None:
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, db_item)