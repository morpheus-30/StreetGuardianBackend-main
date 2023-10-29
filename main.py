import mysql.connector
from flask import *
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from flask_ngrok import run_with_ngrok
import geopy.distance
import json
import ai
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='sgdb'
)
db = mydb.cursor(dictionary=True)
headers = {
    'Access-Control-Allow-Origin': '*'
}
app = Flask(__name__)
run_with_ngrok(app)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['POST', "GET"])
def home():
    return jsonify({'status': 200, 'message': "SWAGAT H AAPKA SHREEMATI CHIRAG MAHODAYA"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db.execute("SELECT id FROM User WHERE mobile = %s AND password = %s",
               (data['mobile'], data['password']))
    user = db.fetchone()
    if user:
        return jsonify({"data": user["uid"], 'status': 200})
    else:
        return jsonify({"data": False, 'status': 404})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    db.execute("SELECT * FROM User WHERE mobile = %s AND password = %s",
               (data['mobile'], data['password']))
    user = db.fetchone()
    if user:
        return jsonify({'status': 404, 'message': "User already exists"})
    db.execute("INSERT INTO User (email, mobile, password) VALUES (%s,%s, %s, %s)",
               (data["email"], data['LatLong'], data['mobile'], data['password']))
    mydb.commit()
    return jsonify({'status': 200, 'message': "User registered successfully"})


@app.route('/iologin', methods=['POST'])
def iologin():
    data = request.get_json()
    db.execute("SELECT * FROM io WHERE mobile = %s AND password = %s",
               (data['mobile'], data['password']))
    user = db.fetchone()
    if user:
        return jsonify({"data": True, 'status': 200})
    else:
        return jsonify({'status': 404})


@app.route('/ioregister', methods=['POST'])
def ioregister():
    data = request.get_json()
    db.execute("SELECT * FROM io WHERE mobile = %s AND password = %s",
               (data['mobile'], data['password']))
    user = db.fetchone()
    if user:
        return jsonify({'status': 404, 'message': "User already exists"})
    db.execute("INSERT INTO io (email, mobile, password, designation, adhaar) VALUES (%s,%s, %s, %s)",
               (data["email"], data['mobile'], data['password'], data['designation'], data['adhaar']))
    mydb.commit()
    return jsonify({'status': 200, 'message': "User registered successfully"})


@app.route('/getReports', methods=['GET'])
def getReports():
    db.execute("SELECT * FROM report ORDER BY upvotes,severity DESC")
    reports = db.fetchall()
    # type(reports)
    return json.dumps({'status': 200, 'data': reports}, default=str)


@app.route('/addReport', methods=['POST'])
def addReport():
    data = request.get_json()
    db.execute(
        "INSERT INTO report (io_id,date,time,LatLong,title,description,vehicle_type,faults,severity) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)", (data["io_id"], data["date"], data["time"], data["LatLong"], data["title"], data["description"], data["vehicle_type"], data["faults"], data["severity"]))
    mydb.commit()
    return jsonify({'status': 200, 'message': "Report added successfully"})


@app.route('/upvote', methods=['POST'])
def upvote():
    data = request.get_json()
    db.execute("SELECT upvoted_reports FROM User where uid = %s",
               (data["uid"]))
    upvoted_reports = db.fetchone()["upvoted_reports"]['data']
    if data["report_id"] not in upvoted_reports:
        db.execute("UPDATE User SET upvoted_reports = %s WHERE uid = %s",
                   (upvoted_reports + data["report_id"], data["uid"]))
        db.execute(
            "UPDATE report SET upvotes = upvotes + 1 WHERE report_id = %s", (data["report_id"]))
        mydb.commit()
    else:
        db.execute("UPDATE User SET upvoted_reports = %s WHERE uid = %s",
                   (upvoted_reports - data["report_id"], data["uid"]))
        db.execute(
            "UPDATE report SET upvotes = upvotes - 1 WHERE report_id = %s", (data["report_id"]))
        mydb.commit()
    return jsonify({'status': 200, 'message': "Upvoted successfully"})


@app.route('/addPrecautions', methods=['POST'])
def alert():
    data = request.get_json()
    db.execute("INSERT INTO precautions (report_id,data) VALUES (%s,%s)",
               (data["report_id"], data["data"]))
    return jsonify({'status': 200, 'message': "Precautions added successfully"})


@app.route('/getPrecautions', methods=['GET'])
def getPrecautions():
    prompt = request.args.get('prompt')
    precautions = ai.ask(prompt)
    print(precautions)
    return jsonify({'status': 200, 'data': precautions})

@app.route('/getspots', methods=['GET'])
def getspots():
    result = []
    try:
        lat = float(request.args.get('lat'))
        long = float(request.args.get('long'))
        db.execute("SELECT severity,faults,LatLong FROM report")       
        
        spots = db.fetchall()
        # print(spots)
        for spot in spots:
            data =  json.loads(spot['LatLong'])
            if(abs(geopy.distance.distance((data['Lat'], data['Long']), (lat,long) ).m)<1000):
                    result.append(spot)
        print(result)
        return json.dumps({'status': 200, 'data': result}, default=str)
    except:
        return jsonify({'status': 333, 'data': "Error"})
app.run(debug=True)
