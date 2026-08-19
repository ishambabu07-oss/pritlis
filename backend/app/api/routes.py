import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.models.schemas import SatelliteRecord, ConjunctionAlert
from app.data.fetch_tles import fetch_active_catalog
from app.core.filters import filter_apogee_perigee
from app.core.tca_solver import find_tca_between_pair
from app.services.risk_scorer import calculate_conjunction_risk

router = APIRouter()

# In-memory catalog cache
CATALOG_CACHE: List[SatelliteRecord] = []

@router.post("/catalog/refresh", response_model=dict)
def refresh_catalog(group: str = Query("active", description="CelesTrak group")):
    global CATALOG_CACHE
    try:
        CATALOG_CACHE = fetch_active_catalog(group)
        return {"status": "success", "total_objects": len(CATALOG_CACHE), "group": group}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/catalog", response_model=List[SatelliteRecord])
def get_catalog(limit: int = Query(100, ge=1, le=2000)):
    return CATALOG_CACHE[:limit]

@router.get("/conjunctions/scan", response_model=List[ConjunctionAlert])
def run_conjunction_scan(
    max_candidates: int = Query(50, description="Limit processed catalog size for demo latency"),
    miss_distance_cutoff_km: float = Query(25.0, description="Flag approaches under this threshold")
):
    if not CATALOG_CACHE:
        raise HTTPException(status_code=400, detail="Catalog is empty. Call /api/catalog/refresh first.")
    
    subset = CATALOG_CACHE[:max_candidates]
    # Step 1: Apogee-Perigee Filter
    candidate_indices = filter_apogee_perigee(subset, altitude_buffer_km=miss_distance_cutoff_km)
    
    alerts: List[ConjunctionAlert] = []
    now = datetime.now(timezone.utc)

    for i, j in candidate_indices:
        sat1 = subset[i]
        sat2 = subset[j]

        # Step 2 & 3: TCA Solver
        conjunction = find_tca_between_pair(sat1, sat2, start_time=now, duration_hours=12.0)

        if conjunction["miss_distance_km"] <= miss_distance_cutoff_km:
            risk_score, risk_level = calculate_conjunction_risk(
                conjunction["miss_distance_km"],
                conjunction["relative_velocity_km_s"],
                sat1.bstar_drag,
                sat2.bstar_drag
            )

            alerts.append(ConjunctionAlert(
                id=str(uuid.uuid4())[:8],
                sat1_id=sat1.norad_id,
                sat1_name=sat1.name,
                sat2_id=sat2.norad_id,
                sat2_name=sat2.name,
                tca_utc=conjunction["tca_utc"],
                miss_distance_km=conjunction["miss_distance_km"],
                relative_velocity_km_s=conjunction["relative_velocity_km_s"],
                risk_score=risk_score,
                risk_level=risk_level
            ))

    # Sort alerts by highest risk first
    alerts.sort(key=lambda a: a.risk_score, reverse=True)
    return alerts