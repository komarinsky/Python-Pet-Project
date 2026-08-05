from sqlalchemy import select
from sqlalchemy.orm import Session

from pet_project import models, schemas


def create_shipment(db: Session, shipment: schemas.ShipmentCreate) -> models.Shipment:
    db_shipment = models.Shipment(**shipment.model_dump())
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


def get_shipment(db: Session, shipment_id: int) -> models.Shipment | None:
    return db.get(models.Shipment, shipment_id)


def get_shipments(db: Session) -> list[models.Shipment]:
    return list(db.scalars(select(models.Shipment)).all())


def update_shipment(
    db: Session, db_shipment: models.Shipment, shipment: schemas.ShipmentCreate
) -> models.Shipment:
    db_shipment.tracking_number = shipment.tracking_number
    db_shipment.country_from = shipment.country_from
    db_shipment.country_to = shipment.country_to
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


def delete_shipment(db: Session, db_shipment: models.Shipment) -> None:
    db.delete(db_shipment)
    db.commit()


def create_item(db: Session, item: schemas.ItemCreate, shipment_id: int) -> models.Item:
    db_item = models.Item(**item.model_dump(), shipment_id=shipment_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int) -> models.Item | None:
    return db.get(models.Item, item_id)


def get_items(db: Session) -> list[models.Item]:
    return list(db.scalars(select(models.Item)).all())


def update_item(db: Session, db_item: models.Item, item: schemas.ItemCreate) -> models.Item:
    db_item.name = item.name
    db_item.weight = item.weight
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, db_item: models.Item) -> None:
    db.delete(db_item)
    db.commit()