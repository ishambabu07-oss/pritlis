from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SatelliteRecord(BaseModel):
    norad_id: int
    name: str
    line1: str
    line2: str
    apogee_km: float
    perigee_km: float
    inclination_deg: float
    bstar_drag: float

class SatellitePosition(BaseModel):
    norad_id: int
    name: str
    timestamp: datetime
    x_km: float
    y_km: float
    z_km: float
    latitude_deg: float
    longitude_deg: float
    altitude_km: float

class ConjunctionAlert(BaseModel):
    id: str
    sat1_id: int
    sat1_name: str
    sat2_id: int
    sat2_name: str
    tca_utc: datetime
    miss_distance_km: float
    relative_velocity_km_s: float
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"