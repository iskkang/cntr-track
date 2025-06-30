from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from track_one import track_one
from track_maersk import track_maersk
from track_cma import track_cma

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    html_path = os.path.join(app.static_folder, 'index.html')
    if os.path.exists(html_path):
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return '🛳 컨테이너 추적 API 서버입니다. POST /api/track 으로 요청하세요.'

@app.route('/api/track', methods=['POST'])
def track_container():
    data = request.get_json()
    carrier = data.get('carrier', '').upper()
    container_number = data.get('container_number', '').strip()

    if carrier == "ONE":
        return jsonify(track_one(container_number))
    elif carrier == "MAERSK":
        return jsonify(track_maersk(container_number))
    elif carrier == "CMA-CGM":
        return jsonify(track_cma(container_number))
    else:
        return jsonify({
            'success': False,
            'error': f"{carrier}는 아직 지원되지 않습니다. 지원 해운사: ONE, MAERSK, CMA-CGM"
        })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})
