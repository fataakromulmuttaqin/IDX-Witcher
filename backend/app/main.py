from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.errors import ApiError
from app.routers import feed, market_map, meta, portfolio, screens, screener, stocks, watchlists
from core.config import get_settings

cfg = get_settings()
app = FastAPI(
    title="IDX Witcher API",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.exception_handler(ApiError)
async def api_error_handler(_: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


for module in (meta, market_map, stocks, screener, screens, watchlists, feed, portfolio):
    app.include_router(module.router, prefix="/api/v1")
