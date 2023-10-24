import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
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
        score = db.execute("SELECT * FROM score WHERE id = ?" , id)[0]
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

@app.route("/regis", methods=["GET","POST"])
def regis_data():
    
    """Register user"""
    if request.method == "POST":
        if not request.form.get("Name"):
            return "must provide Name"
        elif not request.form.get("Password"):
            return "must provide Password"
        rows = db.execute("SELECT * FROM users WHERE Name = ?", request.form.get("Name"))
        Email = request.form.get("Email")
        Name = request.form.get("Name")
        Password = request.form.get("Password")
        regpassword = request.form.get("regpassword")
        hash = generate_password_hash(Password)
        if len(rows) == 1:
            return "Name already taken"
        if Password == regpassword:
            db.execute("INSERT INTO users(Name, hash) VALUES(?, ?)", Name, hash)
            registered_user = db.execute("SELECT * FROM user where Name = ?", Name)
            session["id"] = registered_user[0]["id"]
            flash('You are successfully registered')
            return redirect("/")
        else:
            return "must provide matching password"   
    else:
        return render_template("regis.html")
        
    