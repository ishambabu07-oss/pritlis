import math
from typing import List
from app.models.schemas import SatelliteRecord

# Constants for Astrodynamics
MU_EARTH = 398600.4418  # Earth's gravitational parameter (km^3/s^2)
EARTH_RADIUS_KM = 6378.137

def parse_scientific_notation(val_str: str) -> float:
    """Parses TLE scientific notation (e.g., ' 30122-3' -> 0.00030122)."""
    val_str = val_str.strip()
    if not val_str or val_str == "00000-0" or val_str == "00000+0":
        return 0.0
    
    sign = -1.0 if val_str.startswith('-') else 1.0
    val_str = val_str.lstrip('+- ')
    
    if '-' in val_str:
        mantissa, exp = val_str.split('-')
        exp = -int(exp)
    elif '+' in val_str:
        mantissa, exp = val_str.split('+')
        exp = int(exp)
    else:
        return float(val_str)
        
    return sign * float(f"0.{mantissa}") * (10 ** exp)

def parse_tle_catalog(raw_text: str) -> List[SatelliteRecord]:
    """Converts a raw multi-line TLE string into a list of validated SatelliteRecords."""
    lines = [l.strip() for l in raw_text.strip().splitlines() if l.strip()]
    records = []
    i = 0
    
    while i < len(lines):
        # Handle 2-line or 3-line format
        if lines[i].startswith("1 ") and i + 1 < len(lines) and lines[i+1].startswith("2 "):
            name = f"OBJECT_{lines[i][2:7].strip()}"
            l1, l2 = lines[i], lines[i+1]
            i += 2
        elif i + 2 < len(lines) and lines[i+1].startswith("1 ") and lines[i+2].startswith("2 "):
            name = lines[i]
            l1, l2 = lines[i+1], lines[i+2]
            i += 3
        else:
            i += 1
            continue

        try:
            norad_id = int(l1[2:7])
            inclination = float(l2[8:16])
            eccentricity = float("0." + l2[26:33].strip())
            mean_motion_rev_day = float(l2[52:63])
            bstar_str = l1[53:61]
            bstar = parse_scientific_notation(bstar_str)

            # Compute semi-major axis (a), perigee, and apogee using Kepler's 3rd Law
            n_rad_s = mean_motion_rev_day * (2 * math.pi / 86400.0)
            a_km = (MU_EARTH / (n_rad_s ** 2)) ** (1.0 / 3.0)
            
            perigee_km = a_km * (1.0 - eccentricity) - EARTH_RADIUS_KM
            apogee_km = a_km * (1.0 + eccentricity) - EARTH_RADIUS_KM

            records.append(SatelliteRecord(
                norad_id=norad_id,
                name=name,
                line1=l1,
                line2=l2,
                apogee_km=apogee_km,
                perigee_km=perigee_km,
                inclination_deg=inclination,
                bstar_drag=bstar
            ))
        except Exception:
            continue
            
    return records