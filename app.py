from flask import Flask, request, render_template
from main import getsymptoms,getData
import sqlite3
app=Flask(__name__)

DATABASE = 'users_info.db'
username=""
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
    if user:
        symptoms=getsymptoms()
        global username
        email,username,password=user
        return render_template("second_page.html",username=username,symptoms=symptoms) 
    else:
        error="Crendentials doesn't match"
        return render_template("homepage.html",error=error)

@app.route('/signup', methods=['POST'])
def signup():
    global username
    username=request.form['username']
    email = request.form['email']
    password = request.form['password']
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        connection.commit()
    symptoms=getsymptoms()
    return render_template("second_page.html",username=username,symptoms=symptoms)

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route('/predict',methods=['post'])
def predict():
    if request.method=='POST':
        syms=[sym for sym in request.form.values()]
        diseases,description,precaution,message=getData(syms)
        return render_template('predicted.html',diseases=diseases,description=description,precaution=precaution,message=message,username=username)

@app.route('/predictpage')
def predictpage():
    symptoms=getsymptoms()
    return render_template("second_page.html",username=username,symptoms=symptoms)

@app.route('/contactpage')
def contactpage():
    return render_template("contact.html",username=username)

@app.route('/aboutpage')
def aboutpage():
    return render_template("about.html",username=username)

app.static_folder='static'

if __name__=='__main__':
    app.run(debug=True)