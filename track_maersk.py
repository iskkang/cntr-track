import requests
from bs4 import BeautifulSoup
from datetime import datetime

def track_maersk(container_number):
    url = f"https://www.maersk.com/tracking/{container_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/125.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return {
                "success": False,
                "status": "페이지 요청 실패",
                "code": response.status_code
            }

        soup = BeautifulSoup(response.text, "html.parser")

        # 🟡 예시: 가장 마지막 상태 이벤트 찾기 (개발자 도구에서 구조를 보고 조정 필요)
        status_div = soup.find("div", class_="shipment__event-description")
        time_div = soup.find("span", class_="shipment__event-datetime")

        if not status_div or not time_div:
            return {
                "success": True,
                "carrier": "MAERSK",
                "container_number": container_number,
                "status": "상태 정보 없음",
                "current_location": "위치 정보 없음",
                "last_update": datetime.utcnow().isoformat(),
                "source": url
            }

        return {
            "success": True,
            "carrier": "MAERSK",
            "container_number": container_number,
            "status": status_div.get_text(strip=True),
            "current_location": "웹페이지 내 표시된 항만 또는 도시",
            "last_update": datetime.utcnow().isoformat(),
            "source": url
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
