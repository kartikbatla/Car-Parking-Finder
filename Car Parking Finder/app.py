from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
from geopy.geocoders import Nominatim
import main

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('databases.db') 
    c = conn.cursor()

    # Create the tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    location TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS parking_spots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('Available', 'Occupied')),
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS parking_detection_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    parking_spot_id INTEGER,
                    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    result TEXT NOT NULL,
                    FOREIGN KEY (parking_spot_id) REFERENCES parking_spots(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS user_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    parking_spot_id INTEGER,
                    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    request_status TEXT NOT NULL CHECK(request_status IN ('Pending', 'Confirmed', 'Rejected')),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (parking_spot_id) REFERENCES parking_spots(id))''')

    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('Frame5.html')

@app.route('/check_parking')
def check_parking():
    # Example for calling your parking detection code
    video_feed = main.run_parking_detection()
    return Response(video_feed, mimetype='video/mp4')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    location = request.form['location']
    
    # Save to database
    conn = sqlite3.connect('database/parking_detection.db')  # Path to DB
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, location) VALUES (?, ?, ?)", (name, email, location))
    conn.commit()
    conn.close()
    
    # Geocode location
    geolocator = Nominatim(user_agent="myGeocoder")
    location_data = geolocator.geocode(location)
    map_url = f"https://www.google.com/maps?q={location_data.latitude},{location_data.longitude}"

    return redirect(map_url)

if __name__ == '__main__':
    app.run(debug=True)
