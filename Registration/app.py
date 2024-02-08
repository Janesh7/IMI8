from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import re
import logging

app = Flask(__name__)

app.secret_key = 'your_secret_key'
logging.basicConfig(level=logging.INFO)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql@123',
    'database': 'test',
    'auth_plugin': 'mysql_native_password'  # This may be needed depending on your MySQL version
}

try:
    mysql_connection = mysql.connector.connect(**db_config)
    logging.info("MySQL connection established successfully.")
except Exception as e:
    logging.error(f"Failed to establish MySQL connection: {e}")

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'DateOfBirth' in request.form:
        username = request.form['username']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        address = request.form['address']
        DateOfBirth = request.form['DateOfBirth']
        cursor = mysql_connection.cursor()  # Use mysql_connection here
        cursor.execute('SELECT * FROM registration WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO registration (username, email, phoneNumber, address, DateOfBirth) VALUES (%s, %s, %s, %s, %s)', (username, email, phoneNumber, address, DateOfBirth))
            mysql_connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route("/display", methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        filter_key = request.form.get('filter_key', None)
        filter_value = request.form.get('filter_value', None)
        if filter_key and filter_value:
            query = f"SELECT id, username, email, phoneNumber, address, DateOfBirth, CreatedAt, UpdatedAt FROM registration WHERE {filter_key} LIKE '%{filter_value}%'"
        else:
            query = "SELECT id, username, email, phoneNumber, address, DateOfBirth, CreatedAt, UpdatedAt FROM registration"
    else:
        query = "SELECT id, username, email, phoneNumber, address, DateOfBirth, CreatedAt, UpdatedAt FROM registration"
    
    cursor = mysql_connection.cursor(dictionary=True)
    cursor.execute(query)
    accounts = cursor.fetchall()
    cursor.close()

    return render_template("display.html", accounts=accounts)




@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phoneNumber = request.form.get('phoneNumber')
        address = request.form.get('address')
        DateOfBirth = request.form.get('DateOfBirth')
        
        # Check if the username exists
        cursor = mysql_connection.cursor()
        cursor.execute('SELECT * FROM registration WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if not account:
            msg = 'Account does not exist!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            # Update the user's information
            cursor.execute('UPDATE registration SET email = %s, phoneNumber = %s, address = %s, DateOfBirth = %s WHERE username = %s', (email, phoneNumber, address, DateOfBirth, username))
            mysql_connection.commit()
            msg = 'You have successfully updated!'
            
    return render_template("update.html", msg=msg)

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        username = request.form['username']
        cursor = mysql_connection.cursor()

        # Check if the username exists in the database
        cursor.execute("SELECT * FROM registration WHERE username = %s", (username,))
        account = cursor.fetchone()

        if account:
            try:
                cursor.execute("DELETE FROM registration WHERE username = %s", (username,))
                mysql_connection.commit()
                flash('User deleted successfully', 'success')
            except mysql.connector.Error as err:
                flash(f'Error: {err}', 'error')
        else:
            flash('User does not exist', 'error')

        cursor.close()
        return redirect(url_for('delete'))

    return render_template("delete.html")



if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
