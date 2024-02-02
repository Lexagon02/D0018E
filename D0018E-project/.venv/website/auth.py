from flask import Blueprint, render_template, request
import pymysql.cursors
connection = pymysql.connect(host='d0018e-database.cvwk6aiy4nnq.eu-north-1.rds.amazonaws.com',
                             user='admin',
                             password='ltu1234567',
                             database='database',
                             cursorclass=pymysql.cursors.DictCursor)

auth = Blueprint('auth', __name__)



@auth.route("/register", methods = ["GET", "POST"])
def register():
    connection = pymysql.connect(host='d0018e-database.cvwk6aiy4nnq.eu-north-1.rds.amazonaws.com',
                             user='admin',
                             password='ltu1234567',
                             database='database',
                             cursorclass=pymysql.cursors.DictCursor)

    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("fname")
       # getting input with name = fname in HTML form
       surname = request.form.get("sname")
       # getting input with name = fname in HTML form
       mail = request.form.get("mail")
       # getting input with name = fname in HTML form
       address = request.form.get("address")
       # getting input with name = fname in HTML form
       password = request.form.get("pword") 
       with connection:
        with connection.cursor() as cursors:
            # Read a single record
            sql = "INSERT INTO users (name,surname,mail,password,address,isAdmin) VALUES (%s,%s,%s,%s,%s,0);"
            cursors.execute(sql,(first_name,surname,mail,password,address))
            connection.commit()
            
       
       return "Your username is "+ first_name
    return render_template("register.html")

@auth.route("/login", methods = ["GET", "POST"])
def login():
    connection = pymysql.connect(host='d0018e-database.cvwk6aiy4nnq.eu-north-1.rds.amazonaws.com',
                             user='admin',
                             password='ltu1234567',
                             database='database',
                             cursorclass=pymysql.cursors.DictCursor)


    if request.method == "POST":
       # getting input with name = fname in HTML form
       mail = request.form.get("mail")
       # getting input with name = lname in HTML form 
       password = request.form.get("pword") 
       with connection:
            with connection.cursor() as cursorn:
                # Read a single record
                sql = "SELECT name,surname,isAdmin FROM users WHERE mail = %s AND password = %s"
                cursorn.execute(sql,(mail,password))
                result = cursorn.fetchall()
            return render_template("profile.html", data=result)
    else:
        return render_template("login.html")

@auth.route("/profile", methods = ["GET", "POST"])
def profile():
    return render_template("profile.html")

@auth.route("/adminStuff", methods = ["GET", "POST"])
def adminStuff():
    return render_template("adminStuff.html")