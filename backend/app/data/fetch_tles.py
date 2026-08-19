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
        "Accept": "text/plain, application/octet-stream, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://celestrak.org/"
    }

    try:
        print(f"[DEBUG] Requesting TLE catalog from: {url}")
        res = requests.get(url, headers=headers, timeout=15)
        print(f"[DEBUG] HTTP Status: {res.status_code}")
        print(f"[DEBUG] Content-Type: {res.headers.get('Content-Type', 'unknown')}")
        print(f"[DEBUG] Response Preview: {res.text[:200]}...")
        res.raise_for_status()

        response_text = res.text.strip()
        if "<html" in response_text.lower():
            print("[ERROR] CelesTrak returned HTML instead of TLE data. Request may have been blocked.")
            return []

        return parse_tle_catalog(response_text)

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch TLE data from CelesTrak: {e}")
        return []