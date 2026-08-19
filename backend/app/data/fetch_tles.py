import requests
from typing import List
from app.models.schemas import SatelliteRecord
from app.data.parser import parse_tle_catalog

def fetch_active_catalog(group: str = "active") -> List[SatelliteRecord]:
    """
    Fetches the real-time orbital catalog from CelesTrak.
    Delegates the heavy string parsing to parser.py.
    """
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"
    
    # Disguise the request as a standard Chrome browser to bypass bot-blockers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/plain"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        
        # Debugging: Print the first 100 characters to ensure it's actually TLE data and not HTML
        print(f"[DEBUG] CelesTrak Response Start: \n{res.text[:100]}...\n")
        
        return parse_tle_catalog(res.text)
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch TLE data from CelesTrak: {e}")
        return []