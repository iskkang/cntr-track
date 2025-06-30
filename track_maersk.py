import requests

def track_maersk(container_number):
    url = f"https://api.maersk.com/synergy/tracking/{container_number}?operator=MAEU"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/125.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Origin": "https://www.maersk.com",
    "Referer": f"https://www.maersk.com/tracking/{container_number}",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}


    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"success": False, "status": "API 호출 실패", "code": response.status_code}

        data = response.json()
        container_data = data['containers'][0]

        result = {
            "carrier": "MAERSK",
            "container_number": container_number,
            "origin": data.get("origin", {}).get("city", ""),
            "destination": data.get("destination", {}).get("city", ""),
            "current_status": container_data.get("status", "정보 없음"),
            "eta": container_data.get("eta_final_delivery", ""),
            "last_event": container_data.get("locations", [])[-1]['events'][-1],
            "last_update": container_data.get("last_update_time", ""),
            "success": True,
            "source": url
        }
        return result

    except Exception as e:
        return {"success": False, "error": str(e)}
