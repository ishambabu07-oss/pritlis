import numpy as np
from datetime import datetime, timezone
from skyfield.api import load, EarthSatellite, wgs84
from app.models.schemas import SatelliteRecord

# Load the timescale once globally to prevent massive overhead on each function call
ts = load.timescale()

def propagate_satellite_state(sat_record: SatelliteRecord, dt_utc: datetime) -> dict:
    """
    Calculates orbital state at a specific timestamp.
    Returns both ECI coordinates (for collision math) and Geodetic (for UI).
    """
    t = ts.from_datetime(dt_utc.replace(tzinfo=timezone.utc))
    sat = EarthSatellite(sat_record.line1, sat_record.line2, sat_record.name, ts)
    
    # 1. Native ECI state (Earth-Centered Inertial)
    geocentric = sat.at(t)
    pos_eci_km = geocentric.position.km
    vel_eci_km_s = geocentric.velocity.km_per_s
    
    # 2. Convert to Geodetic / ECEF (Latitude, Longitude, Altitude)
    geodetic = wgs84.subpoint_of(geocentric)
    
    return {
        "pos_eci_km": pos_eci_km,
        "vel_eci_km_s": vel_eci_km_s,
        "latitude_deg": geodetic.latitude.degrees,
        "longitude_deg": geodetic.longitude.degrees,
        "altitude_km": geodetic.elevation.km
    }