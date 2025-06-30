from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/track', methods=['POST'])
def track_container():
    data = request.get_json()
    carrier = data.get('carrier')
    container_number = data.get('container_number')
    return jsonify({
        'success': True,
        'carrier': carrier,
        'container_number': container_number,
        'status': '데모 응답입니다',
        'current_location': 'Busan Port',
        'last_update': '2025-06-28T00:00:00Z'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
