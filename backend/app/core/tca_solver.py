import numpy as np
from datetime import datetime, timedelta, timezone
from scipy.optimize import minimize_scalar
from skyfield.api import load, EarthSatellite
from app.models.schemas import SatelliteRecord
ts = load.timescale()

def find_tca_between_pair(sat1: SatelliteRecord, sat2: SatelliteRecord, start_time: datetime, duration_hours: float = 12.0):
    """
    Finds the exact Time of Closest Approach (TCA), minimum miss distance, 
    and relative velocity using bounded 1D numerical optimization.
    """
    sat1_obj = EarthSatellite(sat1.line1, sat1.line2, sat1.name, ts)
    sat2_obj = EarthSatellite(sat2.line1, sat2.line2, sat2.name, ts)

    def separation_distance_km(t_seconds_offset: float) -> float:
        current_dt = start_time + timedelta(seconds=t_seconds_offset)
        t = ts.from_datetime(current_dt.replace(tzinfo=timezone.utc))
        pos1 = sat1_obj.at(t).position.km
        pos2 = sat2_obj.at(t).position.km
        return float(np.linalg.norm(pos1 - pos2))

    # 1. Coarse Search: Use a 30-second step so we don't jump over sharp LEO passes
    total_seconds = duration_hours * 3600
    step_seconds = 30.0  
    coarse_times = np.arange(0, total_seconds, step_seconds)
    
    min_dist = float('inf')
    best_coarse_t = 0.0

    for t_sec in coarse_times:
        d = separation_distance_km(t_sec)
        if d < min_dist:
            min_dist = d
            best_coarse_t = t_sec

    # 2. Refine Search: Bracket the minimum using Brent's Method
    bracket_min = max(0.0, best_coarse_t - step_seconds)
    bracket_max = min(total_seconds, best_coarse_t + step_seconds)

    res = minimize_scalar(
        separation_distance_km, 
        bounds=(bracket_min, bracket_max), 
        method='bounded',
        options={'xatol': 1e-4} # Stop when accurate to within 0.1 milliseconds
    )

    tca_seconds = res.x
    exact_miss_distance = res.fun
    tca_utc = start_time + timedelta(seconds=tca_seconds)

    # 3. Compute Relative Velocity exactly at TCA
    tca_ts = ts.from_datetime(tca_utc.replace(tzinfo=timezone.utc))
    vel1 = sat1_obj.at(tca_ts).velocity.km_per_s
    vel2 = sat2_obj.at(tca_ts).velocity.km_per_s
    relative_velocity = float(np.linalg.norm(vel1 - vel2))

    return {
        "tca_utc": tca_utc,
        "miss_distance_km": exact_miss_distance,
        "relative_velocity_km_s": relative_velocity
    }