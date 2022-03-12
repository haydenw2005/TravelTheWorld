import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql.2122.lakeside-cs.org'
app.config['MYSQL_USER'] = 'student2122'
app.config['MYSQL_PASSWORD'] = 'm545CS42122'
app.config['MYSQL_DB'] = '2122project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'dkfhEWUINADSCNDPBCUiehHAYDENlasdWHITEjdba'
mysql = MySQL(app)

#index homepage, checks for session
@app.route('/')
def index():
    if session.get('haydenwhite_username') != None:
        return redirect(url_for('home'))
    return render_template('index.html', username=session.get('haydenwhite_username'))

#signup, checks for if someone has already signed up, otherwise, add to db
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('first')
        lastname = request.form.get('last')
        cursor = mysql.connection.cursor()


        query = 'SELECT id FROM `haydenwhite_users` WHERE username=%s;'
        queryVars = (username,)
        cursor.execute(query, queryVars)
        mysql.connection.commit()
        results = cursor.fetchall()
        if (len(results) >= 1):
            return render_template('signup.html', error=True)

        securedPassword = generate_password_hash(password)
        query = 'INSERT INTO haydenwhite_users(username, password, first, last) VALUES (%s, %s, %s, %s)'
        queryVars = (username,securedPassword,firstname,lastname,)
        cursor.execute(query, queryVars)
        mysql.connection.commit()

        return redirect(url_for('login'))

#login method, sends user to home if right credientials, otherwise, shoot an error
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error=request.args.get('error'))
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = mysql.connection.cursor()
        query = 'SELECT password FROM haydenwhite_users WHERE username=%s'
        queryVars = (username,)
        cursor.execute(query, queryVars)
        mysql.connection.commit()
        results = cursor.fetchall()
        if (len(results) == 1):
            hashedPassword = results[0]['password']
            if check_password_hash(hashedPassword, password):
                session['haydenwhite_username'] = username
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login', error=True))
        else:
            return redirect(url_for('login', error=True))

#logsout, end session
@app.route('/logout')
def logout():
    session.pop('haydenwhite_username', None)
    return redirect(url_for('index'))

#home
@app.route('/home', methods=['GET','POST'])
def home():
    return render_template('home.html', wishlist=getDbCountries(), names=getAllCountries())

#gets all countries in db specific to user
@app.route('/getDbCountries', methods=['POST'])
def getDbCountries():
        cursor = mysql.connection.cursor()
        userId = getId()
        countryData = {}
        query = "SELECT name FROM haydenwhite_countries WHERE user_id=%s;"
        queryVars = (userId,)
        cursor.execute(query, queryVars)
        mysql.connection.commit()
        wishlist = cursor.fetchall()
        for currentName in wishlist:
            coords = []
            query = "SELECT lat FROM haydenwhite_countries WHERE name=%s;"
            queryVars = (currentName["name"],)
            cursor.execute(query, queryVars)
            mysql.connection.commit()
            countryLat = cursor.fetchall()
            coords.append(float(countryLat[0]["lat"]))

            query = "SELECT lon FROM haydenwhite_countries WHERE name=%s;"
            queryVars = (currentName["name"],)
            cursor.execute(query, queryVars)
            mysql.connection.commit()
            countryLon = cursor.fetchall()
            coords.append(float(countryLon[0]["lon"]))
            countryData[currentName["name"]] = coords
        return countryData

#adds country to db
@app.route('/pin/<string:data>', methods=['POST'])
def pin(data):
    cursor = mysql.connection.cursor()
    data = json.loads(data)
    name = data["name"].replace("%20", " ")
    lat = data["lat"]
    long = data["long"]
    userId = getId()
    if (isCountryAvailability(name) == True):
        query = "REPLACE INTO haydenwhite_countries (name,lat,lon,user_id) VALUES (%s,%s,%s,%s);"
        queryVars = (name, lat, long, userId,)
        cursor.execute(query, queryVars)
        mysql.connection.commit()
    return "success O-O"

#checks if country is already in db
def isCountryAvailability(officialName):
    cursor = mysql.connection.cursor()
    query = 'SELECT COUNT(*) FROM haydenwhite_countries WHERE user_id=%s AND name=%s;'
    queryVars = (getId(), officialName,)
    cursor.execute(query, queryVars)
    mysql.connection.commit()
    total = cursor.fetchall()[0]['COUNT(*)']
    if (total != 0):
        return False
    else:
        return True

#deleted countries passed through js
@app.route('/delete/<string:data>', methods=['POST'])
def delete(data):
    data = json.loads(data)
    cursor = mysql.connection.cursor()
    list = ["hi"]
    for i in range(len(data)):
        query = 'DELETE FROM `haydenwhite_countries` WHERE user_id=%s AND name=%s;'
        queryVars = (getId(), data[i]["name"].replace("%20", " "),)
        cursor.execute(query, queryVars)
        mysql.connection.commit()
    return jsonify(list)

#get user session id
def getId():
    cursor = mysql.connection.cursor()
    query = 'SELECT id FROM haydenwhite_users WHERE username=%s'
    queryVars = (session['haydenwhite_username'],)
    cursor.execute(query, queryVars)
    mysql.connection.commit()
    userId = cursor.fetchall()
    return userId[0]['id']

#gets all countries in db
def getAllCountries():
    response = requests.get("https://restcountries.com/v3.1/all")
    jsonResponse = response.json()
    nameGroupings = []
    allCountryNames = []
    for item in range(len(jsonResponse)):
        nameGroupings.append(jsonResponse[item]["name"])
        allCountryNames.append(nameGroupings[item]["common"])
    return allCountryNames

#No repeats in username
