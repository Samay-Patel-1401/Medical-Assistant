from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import pickle
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open("others/db.yaml"))
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]
mysql = MySQL(app)

featureList = ["age", "gender", "cp", "trtbps", "chol", "FBS", "rest_ecg", "thalach", "exang", "oldpeak", "slp", "ca", "thall"]
numeric_cols = ["age", "trtbps", "chol", "thalach", "oldpeak"]

def analyze(req, X1) :
    scaler = pickle.load(open("saved/scaler.pkl", "rb"))
    clf = pickle.load(open("saved/clf.pkl", "rb"))

    X2 = []
    for x in numeric_cols :
        X2.append(float(req.get(x, '0')))

    X2 = scaler.transform([X2])

    j = 0
    X = []
    for i in range(len(featureList)) :
        if featureList[i] in numeric_cols :
            X.append(X2[0][j])
            j = j + 1
        else :
            X.append(X1[i])
    X = [X]

    Y = clf.predict(X)
    return Y[0]

@app.route("/", methods = ["GET", "POST"])
def index() :
    if request.method == "GET" :
        return render_template("index.html")
    elif request.method == "POST" :
        X = []
        for x in featureList :
            X.append(float(request.form.get(x, '0')))
        Y = analyze(request.form, X)

        cur = mysql.connection.cursor()
        cur.execute("SELECT costumer_id FROM records ORDER BY costumer_id DESC LIMIT 1")
        data = cur.fetchall()
        ID = int(data[0][0]) + 1

        s = '"' + str(ID) + '"'
        for x in featureList :
            s = s + ", " + request.form.get(x, '0')

        cur.execute("INSERT INTO records(costumer_id, age , gender, cp, trtbps, chol, FBS, rest_ecg, thalach, exang, oldpeak, slp, ca, thall) VALUES( "+s+")")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('appointment', result=Y, ID=ID))

@app.route("/<int:result>/<int:ID>", methods = ["GET", "POST"])
def appointment(result, ID) :
    if request.method == "GET" :
        comment = "You seem fine."
        color = "color:green"
        if result :
            comment = "You should see a doctor."
            color = "color:red"

        cur = mysql.connection.cursor()
        cur.execute("SELECT doc_id, doc_name, slot_avail FROM doctors")
        data = cur.fetchall()
        cur.close()

        return render_template("appointment.html", result=comment, color=color, data=data)
    else :
        name = request.form.get("name")
        time = request.form.get("time")
        time = time.split(":")
        time = "slot" + str(int(time[0]) - 8)
        date = request.form.get("date")
        no = request.form.get("no")
        email = request.form.get("email")
        doc = request.form.get("doc")

        cur = mysql.connection.cursor()
        cur.execute("SELECT doc_id FROM doctors WHERE doc_name='"+doc+"' LIMIT 1")
        doc = (cur.fetchall())[0][0]
        cur.execute("INSERT INTO appointments(costumer_id, costumer_name, costumer_no, costumer_email, app_slot, app_date, doc_id, ini_cond) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (str(ID), name, no, email, time, date, doc, str(result)))
        mysql.connection.commit()
        cur.close()

        return render_template("done.html")

@app.route("/staff")
def staff() :
    if request.method == "GET" :
        return render_template("staff1.html")


if __name__ == "__main__" :
    app.run(debug = True)
