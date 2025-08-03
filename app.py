from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import uuid


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
    if not data.get("name"):  # Example required field
        return jsonify({"error": "Missing 'name' field"}), 400
    data['id'] = str(uuid.uuid4())
    events.append(data)
    save_to_file()
    return jsonify({"message": "Event added!", "event": data}), 201

# -------------------------
# DELETE event by index
# -------------------------
@app.route('/api/events/<string:id>', methods=['DELETE'])
def delete_event(id):
    global events
    event = next((e for e in events if e['id'] == id), None)
    if event:
        
        events = [e for e in events if e['id'] != id]
        save_to_file()
        return jsonify({"message": "Deleted!", "event": event})
    else:
        return jsonify({"error": "Event not found"}), 404

@app.route('/api/events/<string:id>', methods=['PUT'])
def update_event(id):
    global events
    updated_data = request.get_json()

    for i, e in enumerate(events):
        if e['id'] == id:
            # Preserve the id, overwrite other fields
            updated_data['id'] = id
            events[i] = updated_data
            save_to_file()
            return jsonify({"message": "Updated!", "event": updated_data})

    return jsonify({"error": "Event not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)  
