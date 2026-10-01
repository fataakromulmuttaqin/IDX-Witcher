from sqlalchemy import create_engine
from idxwitcher_api.db.base import Base
from idxwitcher_api.db.session import engine

import idxwitcher_api.db.models  # noqa: F401

print("Using database:", engine.url)
Base.metadata.create_all(engine)
print("Tables created.")
