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
        return '🛳 컨테이너 추적 API 서버입니다.\nPOST /api/track 으로 요청하세요.\n지원 해운사: ONE, MAERSK, CMA-CGM'

@app.route('/api/track', methods=['POST'])
def track_container():
    data = request.get_json()
    carrier = data.get('carrier', '').upper()
    container_number = data.get('container_number', '').strip()

    if not carrier or not container_number:
        return jsonify({
            'success': False,
            'error': 'carrier와 container_number는 필수 입력입니다.'
        })

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
