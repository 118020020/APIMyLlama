from flask import request, jsonify
import requests
from datetime import datetime
from typing import Dict, Any
from utils import Utils

class RateLimiter:
    def __init__(self):
        self.rate_limits: Dict[str, Dict[str, Any]] = {}

class API:
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.utils = Utils(db)
        self.rate_limiter = RateLimiter()
        self.setup_routes()

    def setup_routes(self):
        self.app.before_request(self.rate_limit_middleware)
        self.app.route('/health', methods=['GET'])(self.health_check)
        self.app.route('/generate', methods=['POST'])(self.generate_response)

    def rate_limit_middleware(self):
        if request.path == '/health' and request.method == 'GET':
            return None

        data = request.get_json()
        if not data or 'apikey' not in data:
            return None

        apikey = data['apikey']
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT tokens, last_used, rate_limit, active FROM apiKeys WHERE key = ?",
            (apikey,)
        )
        row = cursor.fetchone()

        if not row:
            return jsonify({'error': 'Invalid API key'}), 403

        if not row['active']:
            return jsonify({'error': 'API key is deactivated'}), 403

        current_time = datetime.now().timestamp() * 1000
        minute = 60000
        rate_limit = row['rate_limit']

        if apikey not in self.rate_limiter.rate_limits:
            self.rate_limiter.rate_limits[apikey] = {
                'tokens': row['tokens'],
                'last_used': datetime.fromisoformat(row['last_used']).timestamp() * 1000
            }

        rate_limit_info = self.rate_limiter.rate_limits[apikey]
        time_elapsed = current_time - rate_limit_info['last_used']

        if time_elapsed >= minute:
            rate_limit_info['tokens'] = rate_limit

        if rate_limit_info['tokens'] > 0:
            rate_limit_info['tokens'] -= 1
            rate_limit_info['last_used'] = current_time
            self.rate_limiter.rate_limits[apikey] = rate_limit_info

            cursor.execute(
                "UPDATE apiKeys SET tokens = ?, last_used = ? WHERE key = ?",
                (rate_limit_info['tokens'], datetime.fromtimestamp(rate_limit_info['last_used']/1000).isoformat(), apikey)
            )
            self.db.commit()
            return None
        else:
            return jsonify({'error': 'Rate limit exceeded. Try again later.'}), 429

    def health_check(self):
        apikey = request.args.get('apikey')
        if not apikey:
            return jsonify({'error': 'API key is required'}), 400

        cursor = self.db.cursor()
        cursor.execute("SELECT key FROM apiKeys WHERE key = ?", (apikey,))
        row = cursor.fetchone()

        if not row:
            print(f'Invalid API key: {apikey}')
            return jsonify({'error': 'Invalid API Key'}), 403

        return jsonify({
            'status': 'API is healthy',
            'timestamp': datetime.now().isoformat()
        })

    def generate_response(self):
        data = request.get_json()
        print('Request body:', data)

        apikey = data.get('apikey')
        if not apikey:
            return jsonify({'error': 'API key is required'}), 400

        cursor = self.db.cursor()
        cursor.execute("SELECT key FROM apiKeys WHERE key = ?", (apikey,))
        row = cursor.fetchone()

        if not row:
            print(f'Invalid API key: {apikey}')
            return jsonify({'error': 'Invalid API Key'}), 403

        try:
            ollama_url = self.utils.get_ollama_url()
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    'model': data.get('model', 'llama2'),
                    'prompt': data.get('prompt'),
                    'stream': data.get('stream', False),
                    'images': data.get('images', []),
                    'raw': data.get('raw', False)
                }
            )
            
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({'error': f'Error from Ollama API: {response.text}'}), response.status_code

        except Exception as e:
            print('Error making request to Ollama API:', str(e))
            return jsonify({'error': 'Error making request to Ollama API'}), 500
