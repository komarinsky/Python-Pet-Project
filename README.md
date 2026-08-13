# Pet Project

Навчальний пет-проєкт на FastAPI + SQLAlchemy: API для обліку відправлень (`Shipment`) та товарів у них (`Item`).

Проєкт на ранній стадії розробки, пишеться поступово. CI/лінтера/тестового раннера поки що немає.

## Стек

- Python >=3.12
- Poetry — керування залежностями (src-layout, пакет `pet_project` у `src/`)
- FastAPI — веб-фреймворк
- Uvicorn — ASGI-сервер
- SQLAlchemy 2.x — ORM
- SQLite — локальна БД (`pet_project.db`, у git не потрапляє)

## Встановлення

```bash
poetry install
```

## Запуск

```bash
poetry run uvicorn pet_project.main:app --reload --port 8000
```

Після запуску:
- `http://127.0.0.1:8000/` — корінь API
- `http://127.0.0.1:8000/docs` — автоматична Swagger UI

Таблиці в БД створюються автоматично при старті (`Base.metadata.create_all`). Міграцій (Alembic) немає — якщо змінюється структура існуючої таблиці, потрібно видалити локальний файл `pet_project.db` і перезапустити сервер (не просто дочекатись `--reload`, а повністю зупинити і запустити процес заново).

## Структура

```
src/pet_project/
├── database.py   # engine, SessionLocal, Base, get_db()
├── models.py     # ORM-моделі: Shipment, Item
├── schemas.py    # Pydantic-схеми (Base/Create/Out)
├── crud.py       # функції читання/запису в БД
└── main.py       # FastAPI-застосунок і роути
tests/            # поки що порожній
```

- **Shipment** (1) → **Item** (багато): `Item.shipment_id` — зовнішній ключ з `ondelete="CASCADE"` на рівні БД + `cascade="all, delete-orphan"` на рівні ORM. Видалення відправлення видаляє всі її товари.
- Товар не може існувати без відправлення, тому створюється через вкладений роут, а не окремий `POST /items`.

## API

### Shipments

| Метод  | Шлях              | Опис                                  |
|--------|-------------------|---------------------------------------|
| POST   | `/shipments`      | створити відправлення                 |
| GET    | `/shipments`      | список усіх відправлень               |
| GET    | `/shipments/{id}` | отримати одне відправлення            |
| PUT    | `/shipments/{id}` | оновити відправлення                  |
| DELETE | `/shipments/{id}` | видалити відправлення (і його товари) |

### Items

| Метод  | Шлях                             | Опис                          |
|--------|----------------------------------|-------------------------------|
| POST   | `/shipments/{shipment_id}/items` | створити товар у відправленні |
| GET    | `/items`                         | список усіх товарів           |
| GET    | `/items/{id}`                    | отримати один товар           |
| PUT    | `/items/{id}`                    | оновити товар                 |
| DELETE | `/items/{id}`                    | видалити товар                |

Усі відповіді повертаються через Pydantic-схеми (`ShipmentOut`, `ItemOut`), відсутній id повертає 404.