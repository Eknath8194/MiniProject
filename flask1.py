from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",         
    password="1234",     
    database="bank_app"
)

cursor = db.cursor(dictionary=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
        user = cursor.fetchone()

        if user:
            return redirect('/dashboard')
        else:
            message = "Invalid username or password!"

    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (uname, pwd))
            db.commit()
            return redirect('/')
        except mysql.connector.IntegrityError:
            message = "Username already exists!"

    return render_template('register.html', message=message)

@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT username, password FROM users")  # fetch username & password
    users = cursor.fetchall()
    return render_template('dashboard.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
