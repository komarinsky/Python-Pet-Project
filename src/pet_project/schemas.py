from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    weight: float


class ItemCreate(ItemBase):
    pass


class ItemOut(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    shipment_id: int


class ShipmentBase(BaseModel):
    tracking_number: str
    country_from: str
    country_to: str


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentOut(ShipmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    items: list[ItemOut] = []