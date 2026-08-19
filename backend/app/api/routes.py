from fastapi import APIRouter

router = APIRouter(prefix="/api")

@router.get("/conjunctions")
def conjunctions():
    return []

@router.get("/tles")
def tles():
    return []
