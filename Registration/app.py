from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import re
import logging
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'your_secret_key'
logging.basicConfig(level=logging.INFO)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ADD_UR_PASSWORD_HERE',
    'database': 'test',
    'auth_plugin': 'mysql_native_password'
}

try:
    mysql_connection = mysql.connector.connect(**db_config)
    logging.info("MySQL connection established successfully.")
except Exception as e:
    logging.error(f"Failed to establish MySQL connection: {e}")

def validate_phone_number(phone_number):
    return bool(re.match(r'^[0-9]{10}$', phone_number))

def validate_date(date_str):
    try:
        dob = datetime.strptime(date_str, '%Y-%m-%d')
        if dob > datetime.now():
            return False
    except ValueError:
        return False
    return True

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phoneNumber = request.form.get('phoneNumber')
        address = request.form.get('address')
        DateOfBirth = request.form.get('DateOfBirth')
        cursor = mysql_connection.cursor()  # Use mysql_connection here
        cursor.execute('SELECT * FROM registration WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        errors = []
        if not all([username, email, phoneNumber, address, DateOfBirth]):
            errors.append('Please fill out all the fields!\n')
        if account:
            errors.append('Account already exists!\n')
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            errors.append('Invalid email address!\n')
        if not re.match(r'[A-Za-z0-9]+', username):
            errors.append('Username must contain only characters and numbers!\n')
        if not validate_phone_number(phoneNumber):
            errors.append('Phone number must contain 10 digits!\n')
        if not validate_date(DateOfBirth):
            errors.append('DOB Cannot be set to future\n')
        
        if errors:
            return render_template('register.html', msg='\n'.join(errors))

        try:
            cursor = mysql_connection.cursor()
            cursor.execute('INSERT INTO registration (username, email, phoneNumber, address, DateOfBirth) VALUES (%s, %s, %s, %s, %s)', (username, email, phoneNumber, address, DateOfBirth))
            mysql_connection.commit()
            return render_template('register.html', msg='You have successfully registered!')
        except mysql.connector.Error as e:
            logging.error(f"Error occurred during registration: {e}")
            return render_template('register.html', msg='Failed to register. Please try again later.')
    
    return render_template('register.html')

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
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phoneNumber = request.form.get('phoneNumber')
        address = request.form.get('address')
        DateOfBirth = request.form.get('DateOfBirth')
        
        errors = []
        if not all([username, email, phoneNumber, address, DateOfBirth]):
            errors.append('Please fill out all the fields!')
        
        if not errors:
            try:
                cursor = mysql_connection.cursor()
                cursor.execute('SELECT * FROM registration WHERE username = %s', (username,))
                account = cursor.fetchone()
                if not account:
                    errors.append('Account does not exist!')
                    return render_template('update.html',msg='\n'.join(errors))
                if re.match(r'[^@]+@[^@]+\.[^@]+', email) is None:
                    errors.append('Invalid email address!')
                if re.match(r'[A-Za-z0-9]+', username) is None:
                    errors.append('Username must contain only characters and numbers!')
                if not validate_phone_number(phoneNumber):
                    errors.append('Phone number must contain 10 digits!')
                if not validate_date(DateOfBirth):
                    errors.append('Invalid date of birth or greater than current date!')
                else:
                    cursor.execute('UPDATE registration SET email = %s, phoneNumber = %s, address = %s, DateOfBirth = %s WHERE username = %s', (email, phoneNumber, address, DateOfBirth, username))
                    mysql_connection.commit()
                    return render_template('update.html', msg='You have successfully updated!')
            except mysql.connector.Error as e:
                logging.error(f"Error occurred during update: {e}")
                errors.append('Failed to update. Please try again later.')
        if errors:
            return render_template('update.html', msg='\n'.join(errors))

    return render_template("update.html")


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        username = request.form['username']
        cursor = mysql_connection.cursor()

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
