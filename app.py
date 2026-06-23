import json
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'despesas.json')

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(entries):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/despesas', methods=['GET'])
def get_despesas():
    return jsonify(load_data())

@app.route('/api/despesas', methods=['POST'])
def add_despesa():
    entry = request.get_json()
    entries = load_data()
    entries.insert(0, entry)
    save_data(entries)
    return jsonify({'ok': True})

@app.route('/api/despesas/<int:entry_id>', methods=['DELETE'])
def delete_despesa(entry_id):
    entries = load_data()
    entries = [e for e in entries if e.get('id') != entry_id]
    save_data(entries)
    return jsonify({'ok': True})

@app.route('/api/despesas/clear', methods=['POST'])
def clear_despesas():
    save_data([])
    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
