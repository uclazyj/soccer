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
        rows = db.execute("SELECT date, name, ts, cancel FROM signup")
        return render_template("index.html", rows = rows)
    name = request.form.get("name")
    now = datetime.now(timezone('EST'))
    ts = now.strftime("%Y-%m-%d %H:%M:%S")

    submit_action = request.form.get('submitAction')
    row = db.execute("SELECT COUNT(*) AS COUNT FROM signup WHERE date = ? AND name = ?", date, name)
    count = row[0]["COUNT"]
    if submit_action == "signup":
        if count == 0:
            db.execute("INSERT INTO signup (date, name, ts, cancel) VALUES(?,?,?,?)", date, name, ts, 0)
        else:
            # TODO: Don't update ts if the user has already signed up. Only do so if the user decides to register again.
            db.execute("UPDATE signup SET cancel = ?, ts = ? WHERE date = ? AND name = ? ",
                       0, ts, date, name)
    else:
        if count == 1:
            # Todo: Don't update ts if the user has already withdrawed.
            db.execute("UPDATE signup SET cancel = ?, ts = ? WHERE date = ? AND name = ? ",
                       1, ts, date, name)
    return redirect(url_for('index'))