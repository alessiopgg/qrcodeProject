from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('locations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS locations
                 (id INTEGER PRIMARY KEY, latitude REAL, longitude REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/add_location', methods=['POST'])
def add_location():
    data = request.json
    print(f"Ricevuto: {data}")
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if latitude and longitude:
        conn = sqlite3.connect('locations.db')
        c = conn.cursor()
        c.execute("INSERT INTO locations (latitude, longitude) VALUES (?, ?)", (latitude, longitude))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

@app.route('/get_locations', methods=['GET'])
def get_locations():
    conn = sqlite3.connect('locations.db')
    c = conn.cursor()
    c.execute("SELECT latitude, longitude, timestamp FROM locations")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
