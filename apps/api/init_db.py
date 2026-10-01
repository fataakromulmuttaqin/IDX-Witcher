import os
from idxwitcher_api.core.config import get_settings
from idxwitcher_api.db.base import Base
from idxwitcher_api.db.session import engine

settings = get_settings()

import idxwitcher_api.db.models  # noqa: F401

print("Using database:", engine.url)
Base.metadata.create_all(engine)
print("CORS origins:", settings.cors_origin_list)
print("Tables created.")
