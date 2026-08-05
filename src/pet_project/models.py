from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pet_project.database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(primary_key=True)
    tracking_number: Mapped[str]
    country_from: Mapped[str]
    country_to: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    items: Mapped[list["Item"]] = relationship(
        back_populates="shipment", cascade="all, delete-orphan"
    )


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    weight: Mapped[float]
    shipment_id: Mapped[int] = mapped_column(
        ForeignKey("shipments.id", ondelete="CASCADE")
    )

    shipment: Mapped["Shipment"] = relationship(back_populates="items")