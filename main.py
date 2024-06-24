import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Configuration for MySQL connection
config = {
    'user': 'root',
    'password': 'Enmanuel001',
    'host': 'localhost',
    'database': 'uservault',
}

def connect_to_mysql():
    """ Connect to MySQL database """
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        pnumber = request.form['pnumber']
        username = request.form['username']
        password = request.form['password']
        
        connection = connect_to_mysql()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO users (name, lastname, pnumber, username, password) VALUES (%s, %s, %s, %s, %s)", (name, lastname, pnumber, username, password))
                connection.commit()
                return redirect(url_for('login'))
            except Error as e:
                print(f"Error inserting record: {e}")
            finally:
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    return render_template('signup.html')

@app.route('/')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = connect_to_mysql()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
                user = cursor.fetchone()
                if user:
                    session['username'] = user['username']
                    return redirect(url_for('home'))
                else:
                    return render_template('login.html', error='Invalid username or password')
            except Error as e:
                print(f"Error fetching user: {e}")
            finally:
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    return render_template('login.html', error=None)



if __name__ == '__main__':
    app.run(debug=True)