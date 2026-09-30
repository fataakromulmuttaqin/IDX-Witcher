"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from IDX Witcher_api.core.config import get_settings
from IDX Witcher_api.db.base import Base
from IDX Witcher_api.db.session import engine
from IDX Witcher_api.routers import (
    health,
    companies,
    prices,
    market,
    screen,
    ingestion,
    foreign_flow,
    brokers,
    corporate_actions,
)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Application lifespan hooks."""
    # Create tables on startup for development convenience
    Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="IDX Witcher backend API for IDX market data and AI portfolio.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(companies.router)
app.include_router(prices.router)
app.include_router(market.router)
app.include_router(screen.router)
app.include_router(ingestion.router)
app.include_router(foreign_flow.router)
app.include_router(brokers.router)
app.include_router(corporate_actions.router)


@app.get("/")
async def root() -> dict:
    return {
        "message": "Welcome to IDX Witcher API",
        "docs": "/docs",
        "health": "/health",
    }
