from flask import Flask, redirect, url_for, render_template, request, send_from_directory, session, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from snippet import get_img
import os
import requests
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = 'KEQING'

limiter = Limiter(app, key_func=get_remote_address)

@app.route("/")
def home():
    return render_template("index.html")

sorts = [
            "quicksort", "bubblesort", "selectionsort", "insertionsort", "radixsort", "heapsort", "gnomesort", "mergesort",
            "bogosort", "shellsort", "shakersort", "bitonicsort", "oddevensort", "combsort", "pancakesort"
        ]

for sort in sorts:
    fname = sort[:-4] + "_" + sort[-4:]

    fun = f"""
@app.route("/{sort}/", methods=["GET"])
def {fname}():
    return render_template("sorts/{sort}.html", audio=session.get("audio", True))"""

    exec(fun)

app.config["MONGO_URI"] = "mongodb://localhost:27017/userFeedbackDB"
mongo = PyMongo(app)

@app.route("/feedback/", methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        userName = request.form.get("name")
        userEmail = request.form.get("email")
        subject = request.form.get("subject")
        userFeedback = request.form.get("feedback")
        if len(userName) == 0 or len(userEmail) == 0 or len(subject) == 0 or len(userFeedback) == 0:
            flash("Please fill in all the fields!")
            return render_template("parents/feedback.html")

        mongo.db.userFeedbackDB.insert_one({"name": userName, "email": userEmail, "subject": subject, "feedback": userFeedback})
        flash("Feedback submitted successfully!")
    
    return render_template("parents/feedback.html")


@app.route("/audio/", methods=["PUT"])
def change_audio():
    session["audio"] = not session.get("audio", True)
    return "", 204

@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == "__main__":
    app.run(debug=True, port = 5001)
