import requests
from bs4 import BeautifulSoup
from datetime import datetime

def track_one(container_number):
    try:
        url = f"https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking?ctrack-field={container_number}&trakNoParam={container_number}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # ✅ 추적 상태
        status_el = soup.select_one("div[data-bind*='ShipmentStatus'] span")
        status = status_el.text.strip() if status_el else "상태 정보 없음"

        # ✅ 현재 위치
        loc_el = soup.select_one("div[data-bind*='CurrentLocation'] span")
        location = loc_el.text.strip() if loc_el else "위치 정보 없음"

        # ✅ 날짜
        date_el = soup.select_one("div[data-bind*='LastUpdateDate'] span")
        last_update = date_el.text.strip() if date_el else datetime.utcnow().isoformat()

        return {
            "success": True,
            "carrier": "ONE",
            "container_number": container_number,
            "status": status,
            "current_location": location,
            "last_update": last_update,
            "source": url
        }

    except Exception as e:
        return {
            "success": False,
            "carrier": "ONE",
            "container_number": container_number,
            "error": str(e)
        }
