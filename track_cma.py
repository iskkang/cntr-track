import requests
from bs4 import BeautifulSoup
from datetime import datetime

def track_cma(container_number):
    try:
        url = f"https://www.cma-cgm.com/eBusiness/tracking/detail/{container_number}"
        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        status_el = soup.select_one(".shipment-status")
        location_el = soup.select_one(".current-location")

        status = status_el.text.strip() if status_el else "상태 정보 없음"
        location = location_el.text.strip() if location_el else "위치 정보 없음"

        return {
            "success": True,
            "carrier": "CMA-CGM",
            "container_number": container_number,
            "status": status,
            "current_location": location,
            "last_update": datetime.utcnow().isoformat(),
            "source": url
        }
    except Exception as e:
        return {
            "success": False,
            "carrier": "CMA-CGM",
            "container_number": container_number,
            "error": str(e)
        }
