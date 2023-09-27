from flask import Flask, render_template, request, jsonify
from datetime import datetime
import psycopg2  # For PostgreSQL database

app = Flask(__name__)

# Database configuration (replace with actual database credentials)
db_config = {
    'dbname': 'your_db_name',
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': 'your_db_host',
    'port': 'your_db_port'
}

# routes and views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_diesel', methods=['POST'])
def record_diesel():
    # Get data from the sensor (replace this with actual sensor data retrieval)
    diesel_level = float(request.form.get('diesel_level'))
    timestamp = datetime.now()

    # Save data to the database
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO diesel_consumption (timestamp, diesel_level) VALUES (%s, %s)", (timestamp, diesel_level))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Diesel level recorded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/view_consumption')
def view_consumption():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM diesel_consumption ORDER BY timestamp DESC LIMIT 10")  # Retrieve the last 10 records
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('view_consumption.html', data=data)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
