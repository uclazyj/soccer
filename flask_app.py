from flask import Flask, redirect, render_template, request, url_for
from cs50 import SQL

from datetime import datetime
from pytz import timezone

app = Flask(__name__)
app.config["DEBUG"] = True


db = SQL("sqlite:////home/zhaoyujian/soccer/soccer.db")

date = "2025-01-01"

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        rows_signup = db.execute("SELECT date, name, ts, cancel FROM signup WHERE cancel = 0 ORDER BY ts")
        rows_withdraw = db.execute("SELECT date, name, ts, cancel FROM signup WHERE cancel = 1 ORDER BY ts")
        return render_template("index.html", rows_signup = rows_signup, rows_withdraw = rows_withdraw)
    name = request.form.get("name")
    if name == "" or name[0] == " ":
        return redirect(url_for('index'))

    now = datetime.now(timezone('EST'))
    ts = now.strftime("%Y-%m-%d %H:%M:%S")

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
    return redirect(url_for('index'))