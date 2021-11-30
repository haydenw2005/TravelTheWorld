#https://docs.mapbox.com/help/tutorials/custom-markers-gl-js/
#https://www.w3schools.com/howto/howto_js_filter_lists.asp
#unique usernames $ long passwords

import requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql.2122.lakeside-cs.org'
app.config['MYSQL_USER'] = 'student2122'
app.config['MYSQL_PASSWORD'] = 'm545CS42122'
app.config['MYSQL_DB'] = '2122project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'dkfhEWUINADSCNDPBCUiehHAYDENlasdWHITEjdba'
mysql = MySQL(app)

@app.route('/')
def index():
    if session.get('haydenwhite_username') != None:
        return redirect(url_for('home'))
    return render_template('index.html', username=session.get('haydenwhite_username'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('first')
        lastname = request.form.get('last')
        securedPassword = generate_password_hash(password)
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO haydenwhite_users(username, password, first, last) VALUES (%s, %s, %s, %s)'
        queryVars = (username,securedPassword,firstname,lastname,)
        cursor.execute(query, queryVars)
        mysql.connection.commit()
        return redirect(url_for('index'))

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

@app.route('/logout')
def logout():
    session.pop('haydenwhite_username', None)
    return redirect(url_for('index'))

@app.route('/home', methods=['GET','POST'])
def home():
    cursor = mysql.connection.cursor()
    userId = getId()
    radioInput = request.form.get('travelList')
    name = request.form.get('name')
    lat = request.form.get('lat')
    long = request.form.get('long')
    if (radioInput == "wishlist" and isCountryAvailability(name) == True):
        query = "REPLACE INTO haydenwhite_countries (name,type,lat,lon,user_id) VALUES (%s,%s,%s,%s,%s);"
        queryVars = (name, radioInput, lat, long, userId,)
        cursor.execute(query, queryVars)
        mysql.connection.commit()

    countryData = {}
    query = "SELECT name FROM haydenwhite_countries WHERE user_id=%s;"
    queryVars = (userId,)
    cursor.execute(query, queryVars)
    mysql.connection.commit()
    wishlist = cursor.fetchall()

    #i = 0
    for currentName in wishlist:
        #i += 1
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



    return render_template('home.html', wishlist=countryData)

@app.route('/search')
def search():
    response = requests.get("https://restcountries.com/v3.1/all")
    jsonResponse = response.json()
    allCountryNames = []
    nameGroupings = []
    for item in range(len(jsonResponse)):
        nameGroupings.append(jsonResponse[item]["name"])
        allCountryNames.append(nameGroupings[item]["common"])
    return render_template('search.html', names=allCountryNames)

@app.route('/info', methods=['GET','POST'])
def info():
    country = request.args.get("country")
    #I know this is repetitve, however, I have no way to pass the list of countries from search.html to info.html.
    response = requests.get("https://restcountries.com/v3.1/all")
    jsonResponse = response.json()
    nameGroupings = []
    allCountryNames = []
    list = []
    for item in range(len(jsonResponse)):
        nameGroupings.append(jsonResponse[item]["name"])
        allCountryNames.append(nameGroupings[item]["common"])
    isIncluded = False
    for item in allCountryNames:
        if (item == country):
            isIncluded = True
    if isIncluded == True:
        foundError = False
        response = requests.get("https://restcountries.com/v3.1/name/" + country)
        jsonResponse = response.json()
        try:
            officialName = jsonResponse[0]["name"]["official"]
        except:
            officialName = "No info"
        try:
            capitals = jsonResponse[0]["capital"][0]
        except:
            capitals = "No info"
        try:
            region = jsonResponse[0]["region"]
        except:
            region = "No info"
        try:
            subregion = jsonResponse[0]["subregion"]
        except:
            subregion = "No info"
        try:
            population = jsonResponse[0]["population"]
        except:
            population = "No info"
        try:
            zone = jsonResponse[0]["timezones"][0]
        except:
            zone = "No info"
        try:
            flag = jsonResponse[0]["flags"]["png"]
        except:
            flag = "No info"
        try:
            lat = jsonResponse[0]["latlng"][0]
        except:
            lat = "No info"
        try:
            long = jsonResponse[0]["latlng"][1]
        except:
            long = "No info"
        try:
            currencies = []
            for item in jsonResponse[0]["currencies"]:
                currencies.append(jsonResponse[0]["currencies"][item]["name"] + ", ")
            #this line of code is quite menacing but all it does is get rid of the last comma.
            currencies[len(currencies)-1] = currencies[len(currencies)-1][:len(currencies[len(currencies)-1])-2]
        except:
            currencies = ["No info"]
        try:
            languages = []
            for item in jsonResponse[0]["languages"]:
                languages.append(jsonResponse[0]["languages"][item] + ", ")
            languages[len(languages)-1] = languages[len(languages)-1][:len(languages[len(languages)-1])-2]
        except:
            languages = ["No info"]
        added = isCountryAvailability(officialName)
    return render_template('info.html', error=foundError, country=country, official=officialName, capital=capitals, region=region, subregion=subregion, currencies=currencies, languages=languages, pop=population, zone=zone, flag=flag, lat=lat, long=long, added=added)

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

def getId():
    cursor = mysql.connection.cursor()
    query = 'SELECT id FROM haydenwhite_users WHERE username=%s'
    queryVars = (session['haydenwhite_username'],)
    cursor.execute(query, queryVars)
    mysql.connection.commit()
    userId = cursor.fetchall()
    return userId[0]['id']
