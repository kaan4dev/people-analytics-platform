from fastapi import APIRouter

router = APIRouter(prefix = "/kpis", tags = ["kpis"])

@router.get("/placeholder")
def placeholder():
    return {"note": "KPIs will be added after curated tables exist."}
