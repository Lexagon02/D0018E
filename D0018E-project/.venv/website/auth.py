from flask import Blueprint, render_template, request, redirect, session
from flask_session import Session
import pymysql.cursors
def connection():
    connection = pymysql.connect(host='d0018e-database.cvwk6aiy4nnq.eu-north-1.rds.amazonaws.com',
                                 user='admin',
                                 password='ltu1234567',
                                 database='database',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
auth = Blueprint('auth', __name__)



@auth.route("/register", methods = ["GET", "POST"])
def register():
    registerCon=connection()

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
       
       with registerCon:
        with registerCon.cursor() as cursors:
            # Read a single record
            sql = "INSERT INTO users (name,surname,mail,password,address,isAdmin) VALUES (%s,%s,%s,%s,%s,0);"
            cursors.execute(sql,(first_name,surname,mail,password,address))
            sql = "SELECT name,surname,isAdmin FROM users WHERE mail = %s AND password = %s"
            cursors.execute(sql,(mail,password))
            result = cursors.fetchall()
            registerCon.commit()
            
       
       return render_template("profile.html", data=result)
    return render_template("register.html")

@auth.route("/login", methods = ["GET", "POST"])
def login():
    loginCon=connection()
    if request.method == "POST":
       # getting input with name = fname in HTML form
       mail = request.form.get("mail")
       # getting input with name = lname in HTML form 
       password = request.form.get("pword") 
       with loginCon:
            with loginCon.cursor() as cursorn:
                # Read a single record
                sql = "SELECT name,surname,isAdmin FROM users WHERE mail = %s AND password = %s"
                cursorn.execute(sql,(mail,password))
                result = cursorn.fetchall()
                if(result==()):
                    return render_template("login.html")
                
            return render_template("profile.html", data=result)
    else:
        return render_template("login.html")

@auth.route("/profile", methods = ["GET", "POST"])
def profile():
    return render_template("profile.html")

@auth.route("/adminStuff", methods = ["GET", "POST"])
def adminStuff():
    adminCon=connection()
    heading = ['Brand', 'Model', 'Size', 'Resolution', 'Price']

    sqlTV =  "SELECT model, brand, size, resolution, price FROM `tv`"
    sqlUser =  "SELECT name, surname, mail, password, address, isAdmin FROM `users`"
    if request.method == "POST":
        if request.form["action"]=="AddTV":
            model = request.form.get("model")
            brand = request.form.get("brand")
            size = request.form.get("size")
            res = request.form.get("res")
            price = request.form.get("price")
            stock = request.form.get("stock") 
            
            with adminCon:
                with adminCon.cursor() as cursoraddTV:
                    # Read a single record
                    sql1 = "INSERT INTO tv (model,brand,size,resolution,price,stock) VALUES (%s,%s,%s,%s,%s,%s);"
                    cursoraddTV.execute(sql1,(model,brand,size,res,price,stock))
                    cursoraddTV.execute(sqlTV)
                    result = cursoraddTV.fetchall()
                    cursoraddTV.execute(sqlUser)
                    userdata= cursoraddTV.fetchall()
                    adminCon.commit() 
            return render_template("adminStuff.html",headings=heading,data=result)
        
        if request.form["action"]=="DeleteTV":
            adminRem=connection()
            model = request.form.get("modelRem")
            with adminRem:
                with adminRem.cursor() as cursorRemTV:
                    sql2 = "DELETE FROM tv WHERE model=%s;"
                    cursorRemTV.execute(sql2,(model))
                    cursorRemTV.execute(sqlTV)
                    result = cursorRemTV.fetchall()
                    cursorRemTV.execute(sqlUser)
                    userdata = cursorRemTV.fetchall()
                    adminRem.commit() 
        if request.form["action"]=="DeleteUser":
            adminRemUser=connection()
            model = request.form.get("mailRem")
            with adminRemUser:
                with adminRemUser.cursor() as cursorRemUser:
                    sql3 = "DELETE FROM users WHERE mail=%s;"
                    cursorRemUser.execute(sql3,(model))
                    cursorRemUser.execute(sqlTV)
                    result = cursorRemUser.fetchall()
                    cursorRemUser.execute(sqlUser)
                    userdata = cursorRemUser.fetchall()
                    adminRemUser.commit() 

       return render_template("adminStuff.html",headings=heading,data=result)
    else:
        with adminCon:
            with adminCon.cursor() as cursorShowTV:
                # Read a single record
                cursorShowTV.execute(sqlTV)
                result = cursorShowTV.fetchall()   
                cursorShowTV.execute(sqlUser)
                userdata = cursorShowTV.fetchall()
                adminCon.commit() 
    return render_template("adminStuff.html",headings=heading,data=result,userdata=userdata)

@auth.route("/cart", methods = ["GET", "POST"])
def cart():
    heading = ['Brand', 'Model', 'Price','Amount']
    cartCon=connection()
    with cartCon:
            with cartCon.cursor() as cursorCart:
                # Read a single record
                result=[]
                sql = "SELECT productid,amount FROM cart WHERE userid = %s"
                cursorCart.execute(sql,1)
                input = cursorCart.fetchall()
                #print(input)
                for i in range(len(input)):
                    sql= "SELECT brand,model,price FROM tv WHERE id = %s"
                    cursorCart.execute(sql,input[i].get('productid'))
                    temp=cursorCart.fetchall()
                    temp[0].update(input[i].items())
                    print(temp[0])
                    result=result+temp
    #print(result)
    if request.method == "POST":
       # getting input with name = fname in HTML form
       mail = request.form.get("mail")
       # getting input with name = lname in HTML form 
       password = request.form.get("pword") 
       return render_template("cart.html", headings=heading,data=result)
    else:
        return render_template("cart.html", headings=heading,data=result)

