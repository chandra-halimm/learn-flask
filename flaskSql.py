from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db-kontak'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL()

# Initialize MySQL with the Flask app
mysql.init_app(app)

# Sample route
@app.route('/')
def index():
    try:
        # Use the existing connection
        conn = mysql.connection.cursor()

        # Execute the query to select all rows from 'kontak'
        conn.execute('SELECT * FROM kontak')

        # Fetch all rows
        hasil = conn.fetchall()

        # Close the database connection
        conn.close()

        # Convert the result to a list of dictionaries for JSON response
        data = [{"id": row[0], "nama": row[1], "kategori": row[2], "dibuat_pada": str(row[3])} for row in hasil]

        return jsonify({"status": "success", "message": "Data fetched successfully", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/tambah', methods=['POST'])
def tambah():
    if request.method == 'POST':
        try:
            # Extract data from JSON in the request
            data = request.json
            nama = data.get('nama')
            kategori = data.get('kategori')

            # Extract the date part from the 'dibuat_pada' string if it exists
            dibuat_pada_str = data.get('dibuat_pada')
            dibuat_pada_date = (
                datetime.strptime(dibuat_pada_str, '%Y-%m-%d').date()
                if dibuat_pada_str
                else datetime.now().date()
            )

            # Use the existing connection
            conn = mysql.connection.cursor()

            # Execute the query to insert data
            conn.execute(
                "INSERT INTO kontak (nama, kategori, dibuat_pada) VALUES (%s, %s, %s)",
                (nama, kategori, dibuat_pada_date),
            )

            # Commit changes to the database
            mysql.connection.commit()

            # Close the database connection
            conn.close()

            return jsonify({"status": "success", "message": "Data inserted successfully"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Invalid request method"})
    

@app.route('/tambah/<int:kontak_id>', methods=['PUT'])
def edit_data(kontak_id):
    if request.method == 'PUT':
        try:
            # Extract data from JSON in the request
            data = request.json
            nama = data.get('nama')
            kategori = data.get('kategori')

            # Extract the date part from the 'dibuat_pada' string if it exists
            dibuat_pada_str = data.get('dibuat_pada')
            dibuat_pada_date = (
                datetime.strptime(dibuat_pada_str, '%Y-%m-%d').date()
                if dibuat_pada_str
                else datetime.now().date()
            )

            # Use the existing connection
            conn = mysql.connection.cursor()

            # Execute the query to update data
            conn.execute(
                "UPDATE kontak SET nama=%s, kategori=%s, dibuat_pada=%s WHERE id=%s",
                (nama, kategori, dibuat_pada_date, kontak_id),
            )

            # Commit changes to the database
            mysql.connection.commit()

            # Close the database connection
            conn.close()

            return jsonify({"status": "success", "message": "Data updated successfully"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Invalid request method"})


@app.route('/tambah/<int:kontak_id>', methods=['DELETE'])
def delete_data(kontak_id):
    if request.method == 'DELETE':
        try:
            # Use the existing connection
            conn = mysql.connection.cursor()

            # Execute the query to delete data
            conn.execute("DELETE FROM kontak WHERE id = %s", (kontak_id,))

            # Commit changes to the database
            mysql.connection.commit()

            # Close the database connection
            conn.close()

            return jsonify({'status': "success", "message": "Data deleted successfully"})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Invalid request method"})
    
if __name__ == '__main__':
    app.run(debug=True)
    
