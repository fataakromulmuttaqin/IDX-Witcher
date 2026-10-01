from sqlalchemy import create_engine
from idxwitcher_api.db.base import Base
from idxwitcher_api.db.session import DATABASE_URL

import idxwitcher_api.db.models  # noqa: F401

print("Using database:", DATABASE_URL)
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
print("Tables created.")
