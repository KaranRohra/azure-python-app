from flask import Flask, render_template, request, redirect
import mysql.connector

# Establishing connection with MySQL
connection = mysql.connector.connect(
    host="edureka-server.mysql.database.azure.com",
    user="edureka",
    password="azure#2001",
    database="python_app",
    port=3306
)

app = Flask(__name__)

# Function to create a new record
@app.route('/create', methods=['GET'])
def create_record():
    name = request.args.get("name")
    age = request.args.get("age")

    cursor = connection.cursor()
    sql = "INSERT INTO records (name, age) VALUES (%s, %s)"
    values = (name, age)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()
    
    return "Record added successfully"


# Function to read all records
@app.route('/')
def read_records():
    cursor = connection.cursor()
    sql = "SELECT * FROM records"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    return str(rows)

# Function to update an existing record
@app.route('/update/<int:record_id>', methods=['GET', 'POST'])
def update_record(record_id):
    
    cursor = connection.cursor()
    
    # Checking record exist or not
    sql = "SELECT * FROM records WHERE id = %s"
    value = (record_id,)
    cursor.execute(sql, value)
    record = cursor.fetchone()
    
    if record:
        # Updating record
        new_name = request.args.get("name")
        new_age = request.args.get("age")

        new_name = record[1] if new_name is None else new_name
        new_age = record[2] if new_age is None else new_age

        sql = "UPDATE records SET name = %s, age = %s WHERE id = %s"
        values = (new_name, new_age, record_id)
        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        return "Record updated successfully"
    
    cursor.close()
    return "Record not found!"
    

    

# Function to delete a record
@app.route('/delete/<int:record_id>')
def delete_record(record_id):
    cursor = connection.cursor()
    sql = "DELETE FROM records WHERE id = %s"
    value = (record_id,)
    cursor.execute(sql, value)
    connection.commit()
    cursor.close()
    
    return "Record deleted successfully"

if __name__ == '__main__':
    app.run()
