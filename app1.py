from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",         # Replace with your MySQL username
        password="Prem@123", # Replace with your MySQL password
        database="labor_management"
    )
    return conn

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index1.html')

# Route to get all labor records
@app.route('/api/labor', methods=['GET'])
def get_labor():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM labor')
    labor_records = cursor.fetchall()
    conn.close()
    return jsonify(labor_records)

# Route to add a new labor record
@app.route('/api/labor', methods=['POST'])
def add_labor():
    new_labor = request.json
    name = new_labor['name']
    age = new_labor['age']
    contact_no = new_labor['contact_no']
    address = new_labor['address']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO labor (name, age, contact_no, address) VALUES (%s, %s, %s, %s)',
                   (name, age, contact_no, address))
    conn.commit()
    conn.close()
    return jsonify(new_labor), 201

# Route to delete a labor record
@app.route('/api/labor/<int:id>', methods=['DELETE'])
def delete_labor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM labor WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
