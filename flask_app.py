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
        rows = db.execute("SELECT date, name, signup_ts FROM signup")
        return render_template("index.html", rows = rows)
    name = request.form["name"]
    now = datetime.now(timezone('EST'))
    db.execute("INSERT INTO signup (date, name, signup_ts, cancel) VALUES(?,?,?,?)", date, name, now.strftime("%Y-%m-%d %H:%M:%S"), 0)
    return redirect(url_for('index'))