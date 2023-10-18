import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

# Data students
db = SQL("sqlite:///score.db")
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        
        name = request.form.get("name")
        score = request.form.get("score")
        print(name)
        print(score)
        db.execute("INSERT INTO score (name, score) VALUES(?, ?)", name , score)
        return redirect("/")
    else: 
        students = db.execute("SELECT * FROM score")
        return render_template("index.html", students=students)
    
@app.route("/edit/<id>", methods=["GET","POST"])
def edit_data(id):
    if request.method=="GET":
        score= db.execute("SELECT * FROM score WHERE id = ?" , id)[0]
        print(score)
        return render_template("edit.html", score=score)
    
    elif request.method=="POST":
        score_name = request.form.get("name")
        score_scor = request.form.get("score")
        db.execute('UPDATE score set name = ?, score = ? where id = ?', score_name, score_scor, id)
        return redirect("/")

@app.route("/delete/<id>", methods=["GET","POST"])
def delete_data(id):
    db.execute("delete from score where id = ?", id)
    return redirect("/")
