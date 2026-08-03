from sqlalchemy.orm import Mapped, mapped_column

from pet_project.database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]