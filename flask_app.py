from flask import Flask, redirect, render_template, request, url_for
from cs50 import SQL

app = Flask(__name__)
app.config["DEBUG"] = True


db = SQL("sqlite:////home/zhaoyujian/soccer/soccer.db")

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        names = db.execute("SELECT name FROM signup_nameonly")
        return render_template("index.html", names = names)
    name = request.form["name"]
    db.execute("INSERT INTO signup_nameonly (name) VALUES(?)", name)
    return redirect(url_for('index'))