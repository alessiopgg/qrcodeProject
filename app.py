from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Configurazione di Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Usa il server SMTP del tuo provider di posta
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cilindromagico2.0@gmail.com'  # Sostituisci con il tuo indirizzo email
app.config['MAIL_PASSWORD'] = 'Sabrina123'  # Recupera la password dalla variabile d'ambiente
app.config['MAIL_DEFAULT_SENDER'] = 'cilindromagico2.0@gmail.com'  # Sostituisci con il tuo indirizzo email

mail = Mail(app)

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

        # Invia un'email con le coordinate
        msg = Message("Nuova posizione condivisa",
                      recipients=["cilindromagico2.0@gmail.com"])  # Sostituisci con l'indirizzo email destinatario
        msg.body = f"Latitudine: {latitude}, Longitudine: {longitude}"
        mail.send(msg)

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
