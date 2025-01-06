from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from cs50 import SQL

from datetime import datetime
from pytz import timezone

app = Flask(__name__)
app.config["DEBUG"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:////home/zhaoyujian/soccer/soccer.db")

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        date = request.args.get("date", default="")
        session["date"] = date
        rows_signup = db.execute("SELECT name, ts, cancel FROM signup WHERE date = ? AND cancel = 0 ORDER BY ts", date)
        rows_withdraw = db.execute("SELECT name, ts, cancel FROM signup WHERE date = ? AND cancel = 1 ORDER BY ts", date)
        return render_template("index.html", date = date, rows_signup = rows_signup, rows_withdraw = rows_withdraw)

    date = session["date"]
    name = request.form.get("name")
    if name == "" or " " in name:
        return redirect(url_for('index', date = date))

    now = datetime.now(timezone('EST'))
    today = now.strftime("%Y-%m-%d")
    ts = now.strftime("%Y-%m-%d %H:%M:%S")

    # Cannot signup / withdraw previous event
    if date < today:
        return redirect(url_for('index', date = date))

    submit_action = request.form.get('submitAction')

    row = db.execute("SELECT * FROM signup WHERE date = ? AND name = ?", date, name)

    if submit_action == "signup":
        if len(row) == 0:
            db.execute("INSERT INTO signup (date, name, ts, cancel) VALUES(?,?,?,?)", date, name, ts, 0)
        elif row[0]["cancel"] == 1:
            db.execute("UPDATE signup SET cancel = ?, ts = ? WHERE date = ? AND name = ? ",
                       0, ts, date, name)
    else:
        if len(row) > 0 and row[0]["cancel"] == 0:
            db.execute("UPDATE signup SET cancel = ?, ts = ? WHERE date = ? AND name = ? ",
                       1, ts, date, name)
    return redirect(url_for('index', date = date))