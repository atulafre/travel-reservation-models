"""
Travel Reservations App Backend
Flask application for managing hotel rooms and reservations.
"""

from flask import Flask, jsonify, request, abort, render_template
import json
import os
from typing import Any, Dict, List, Optional
from uuid import uuid4

app = Flask(__name__)
DATA_FILE = 'data.json'

def read_data() -> Dict[str, Any]:
    """
    Read hotel and reservation data from the JSON file.
    Returns:
        dict: Data containing rooms and reservations.
    """
    if not os.path.exists(DATA_FILE):
        return {"rooms": [], "reservations": []}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data: Dict[str, Any]) -> None:
    """
    Write hotel and reservation data to the JSON file.
    Args:
        data (dict): Data to write.
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    """
    Get a list of available hotel rooms.
    Returns:
        JSON response with rooms list.
    """
    data = read_data()
    return jsonify(data.get('rooms', []))

@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    """
    Get a list of all reservations.
    Returns:
        JSON response with reservations list.
    """
    data = read_data()
    return jsonify(data.get('reservations', []))

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    """
    Create a new reservation.
    Expects JSON body with reservation details.
    Returns:
        JSON response with created reservation or error.
    """
    req_data = request.get_json()
    if not req_data:
        abort(400, description="Missing reservation data.")
    required_fields = {'roomId', 'guestName', 'checkIn', 'checkOut'}
    if not required_fields.issubset(req_data):
        abort(400, description="Missing required reservation fields.")
    data = read_data()
    room = next((r for r in data['rooms'] if r['id'] == req_data['roomId']), None)
    if not room or room['availability'] <= 0:
        abort(400, description="Room not available.")
    # Create reservation
    reservation = {
        "id": str(uuid4()),
        "roomId": req_data['roomId'],
        "guestName": req_data['guestName'],
        "checkIn": req_data['checkIn'],
        "checkOut": req_data['checkOut']
    }
    data['reservations'].append(reservation)
    room['availability'] -= 1
    write_data(data)
    return jsonify(reservation), 201

@app.route('/api/reservations/<reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id: str):
    """
    Cancel an existing reservation by ID.
    Returns:
        JSON response with success or error.
    """
    data = read_data()
    reservation = next((r for r in data['reservations'] if r['id'] == reservation_id), None)
    if not reservation:
        abort(404, description="Reservation not found.")
    room = next((r for r in data['rooms'] if r['id'] == reservation['roomId']), None)
    if room:
        room['availability'] += 1
    data['reservations'] = [r for r in data['reservations'] if r['id'] != reservation_id]
    write_data(data)
    return jsonify({"message": "Reservation cancelled."})

@app.route('/')
def index():
    """
    Serve the main frontend page.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
