from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# -------------------------
# 📂 Load or initialize data
# -------------------------
if os.path.exists('data.json'):
    with open('data.json', 'r') as f:
        events = json.load(f)
else:
    events = []

# -------------------------
# 📝 Helper to save to JSON
# -------------------------
def save_to_file():
    with open('data.json', 'w') as f:
        json.dump(events, f, indent=4)

# -------------------------
# GET all events
# -------------------------
@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(events)

# -------------------------
# POST create new event
# -------------------------
@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    events.append(data)
    save_to_file()
    return jsonify({"message": "Event added!", "event": data}), 201

# -------------------------
# DELETE event by index
# -------------------------
@app.route('/api/events/<int:index>', methods=['DELETE'])
def delete_event(index):
    if 0 <= index < len(events):
        deleted = events.pop(index)
        save_to_file()
        return jsonify({"message": "Deleted!", "event": deleted})
    else:
        return jsonify({"error": "Invalid index"}), 404

# -------------------------
# PUT update by index (for toggle complete & edit)
# -------------------------
@app.route('/api/events/<int:index>', methods=['PUT'])
def update_event(index):
    if 0 <= index < len(events):
        events[index] = request.get_json()
        save_to_file()
        return jsonify({"message": "Updated!", "event": events[index]})
    else:
        return jsonify({"error": "Invalid index"}), 404

if __name__ == '__main__':
    app.run(debug=True)

