# Pet Project

A learning pet project built with FastAPI + SQLAlchemy: an API for tracking shipments (`Shipment`) and the items within them (`Item`).

The project is at an early stage and is being built incrementally. There's no CI/linter/test runner yet.

## Tech stack

- Python >=3.12
- Poetry — dependency management (src-layout, `pet_project` package under `src/`)
- FastAPI — web framework
- Uvicorn — ASGI server
- SQLAlchemy 2.x — ORM
- SQLite — local database (`pet_project.db`, gitignored)

## Installation

```bash
poetry install
```

## Running

```bash
poetry run uvicorn pet_project.main:app --reload --port 8000
```

Once running:
- `http://127.0.0.1:8000/` — API root
- `http://127.0.0.1:8000/docs` — auto-generated Swagger UI

Database tables are created automatically on startup (`Base.metadata.create_all`). There's no migration tool (Alembic) — if the schema of an existing table changes, delete the local `pet_project.db` file and restart the server (fully stop and start the process, not just rely on `--reload`).

## Structure

```
src/pet_project/
├── database.py   # engine, SessionLocal, Base, get_db()
├── models.py     # ORM models: Shipment, Item
├── schemas.py    # Pydantic schemas (Base/Create/Out)
├── crud.py       # DB read/write functions
└── main.py       # FastAPI app and routes
tests/            # currently empty
```

- **Shipment** (1) → **Item** (many): `Item.shipment_id` is a foreign key with `ondelete="CASCADE"` at the DB level plus `cascade="all, delete-orphan"` at the ORM level. Deleting a shipment deletes all of its items.
- An item can't exist without a shipment, so it's created via a nested route rather than a standalone `POST /items`.

## API

### Shipments

| Method | Path              | Description                       |
|--------|-------------------|-----------------------------------|
| POST   | `/shipments`      | create a shipment                 |
| GET    | `/shipments`      | list all shipments                |
| GET    | `/shipments/{id}` | get a single shipment             |
| PUT    | `/shipments/{id}` | update a shipment                 |
| DELETE | `/shipments/{id}` | delete a shipment (and its items) |

### Items

| Method | Path                             | Description                      |
|--------|----------------------------------|----------------------------------|
| POST   | `/shipments/{shipment_id}/items` | create an item within a shipment |
| GET    | `/items`                         | list all items                   |
| GET    | `/items/{id}`                    | get a single item                |
| PUT    | `/items/{id}`                    | update an item                   |
| DELETE | `/items/{id}`                    | delete an item                   |

All responses are returned via Pydantic schemas (`ShipmentOut`, `ItemOut`); a missing id returns 404.