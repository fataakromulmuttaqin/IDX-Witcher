from fastapi import APIRouter

router = APIRouter(tags=["watchlists"])


@router.get("/watchlists")
def list_watchlists():
    return {"data": []}


@router.get("/watchlists/{slug}")
def watchlist(slug: str):
    return {"watchlist": slug, "data": []}
