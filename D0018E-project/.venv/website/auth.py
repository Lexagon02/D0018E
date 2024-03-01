from flask import Blueprint, render_template, request, redirect, session
from flask_session import Session
from datetime import date
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
       session["name"]=mail
       with loginCon:
            with loginCon.cursor() as cursorn:
                # Read a single record
                sql = "SELECT name,surname,isAdmin FROM users WHERE mail = %s AND password = %s"
                cursorn.execute(sql,(mail,password))
                result = cursorn.fetchall()
                if(result==()):
                    return render_template("login.html")
                loginCon.commit()
            return render_template("profile.html", data=result)
    else:
        return render_template("login.html")

@auth.route("/logout", methods = ["GET", "POST"])
def logout():
    session["name"] = None
    return render_template('login.html')

@auth.route("/profile", methods = ["GET", "POST"])
def profile():
    if(session["name"] == None):
        return render_template('login.html')
    profileCon=connection()
    with profileCon:
        with profileCon.cursor() as cursorp:
            if request.method == "GET":
                sql="SELECT * FROM users WHERE mail=%s"
                cursorp.execute(sql,session["name"])
                result=cursorp.fetchall()
                isAdmin=result[0].get('isAdmin')
                return render_template("profile.html",isAdmin=isAdmin,data=result)
            else:
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
                header=["name","surname","mail","password","address"]
                data=[first_name,surname,mail,password,address]
                sql="UPDATE users SET password = 123 WHERE mail=%s"
                for  i in range(5):
                    if data[i] == '':
                        continue
                    cursorp.execute(sql,session["name"])
                profileCon.commit()
                return render_template("profile.html")

@auth.route("/adminStuff", methods = ["GET", "POST"])
def adminStuff():
    adminCon=connection()
    heading = ['Brand', 'Model', 'Size', 'Resolution', 'Price']

    sqlTV =  "SELECT model, brand, size, resolution, price FROM `tv`"
    sqlUser =  "SELECT name, surname, mail, password, address, isAdmin FROM `users`"
    sqlOrder =  "SELECT userid,orderid,date FROM `orders`"
    sqlOrderUser =  "SELECT name, surname, mail, address FROM users WHERE id=%s"
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
                    cursoraddTV.execute(sqlOrder)
                    orderdata = cursoraddTV.fetchall()
                    orderresult=[]
                    for order in orderdata:
                        cursoraddTV.execute(sqlOrderUser,order.get('userid'))
                        temp=cursoraddTV.fetchall()
                        temp[0].update(order)
                        orderresult=orderresult+temp
                    adminCon.commit() 
            
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
                    cursorRemTV.execute(sqlOrder)
                    orderdata = cursorRemTV.fetchall()
                    orderresult=[]
                    for order in orderdata:
                        cursorRemTV.execute(sqlOrderUser,order.get('userid'))
                        temp=cursorRemTV.fetchall()
                        temp[0].update(order)
                        orderresult=orderresult+temp
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
                    cursorRemUser.execute(sqlOrder)
                    orderdata = cursorRemUser.fetchall()
                    orderresult=[]
                    for order in orderdata:
                        cursorRemUser.execute(sqlOrderUser,order.get('userid'))
                        temp=cursorRemUser.fetchall()
                        temp[0].update(order)
                        orderresult=orderresult+temp
                    adminRemUser.commit() 
                    
        if request.form["action"]=="DeleteOrder":
            adminRemUser=connection()
            order = request.form.get("orderRem")
            with adminRemUser:
                with adminRemUser.cursor() as cursorRemUser:
                    sql3 = "DELETE FROM orders WHERE orderid=%s;"
                    cursorRemUser.execute(sql3,(order))
                    cursorRemUser.execute(sqlTV)
                    result = cursorRemUser.fetchall()
                    cursorRemUser.execute(sqlUser)
                    userdata = cursorRemUser.fetchall()
                    cursorRemUser.execute(sqlOrder)
                    orderdata = cursorRemUser.fetchall()
                    orderresult=[]
                    for order in orderdata:
                        cursorRemUser.execute(sqlOrderUser,order.get('userid'))
                        temp=cursorRemUser.fetchall()
                        temp[0].update(order)
                        orderresult=orderresult+temp
                    adminRemUser.commit()
                    
        return render_template("adminStuff.html",headings=heading,data=result,userdata=userdata,orderdata=orderresult) 
    else:
        with adminCon:
            with adminCon.cursor() as cursorShowTV:
                # Read a single record
                cursorShowTV.execute(sqlTV)
                result = cursorShowTV.fetchall()   
                cursorShowTV.execute(sqlUser)
                userdata = cursorShowTV.fetchall()
                cursorShowTV.execute(sqlOrder)
                orderdata = cursorShowTV.fetchall()
                orderresult=[]
                for order in orderdata:
                    cursorShowTV.execute(sqlOrderUser,order.get('userid'))
                    temp=cursorShowTV.fetchall()
                    temp[0].update(order)
                    orderresult=orderresult+temp
                adminCon.commit() 
    return render_template("adminStuff.html",headings=heading,data=result,userdata=userdata,orderdata=orderresult)

@auth.route("/cart", methods = ["GET", "POST"])
def cart():
    if not session.get("name"):
        return render_template("login.html")
    mail=session['name']
    heading = ['Brand', 'Model', 'Price','Amount']
    cartCon=connection()
    with cartCon:
            with cartCon.cursor() as cursorCart:
                # Read a single record
                result=[]
                print(mail)
                sql = "SELECT id FROM users WHERE mail = %s"
                cursorCart.execute(sql,mail)
                uid = cursorCart.fetchall()
                uid =uid[0].get('id')
                sql = "SELECT MAX(orderid) FROM orders"
                cursorCart.execute(sql)
                oid = cursorCart.fetchall()
                oid = oid[0].get('MAX(orderid)')
                if(oid==None):
                    oid=1
                sql = "SELECT productid,amount FROM cart WHERE userid = %s"
                cursorCart.execute(sql,uid)
                input = cursorCart.fetchall()
                if request.method == "POST":
                    sql = "INSERT INTO orders (orderid,userid,date,productid,amount) VALUES(%s,%s,%s,%s,%s)"
                    sqlrem="DELETE FROM cart WHERE userid=%s"
                    sqlremstock="UPDATE tv SET stock=stock-%s WHERE productid=%s AND stock>0"
                    
                    for i in range(len(input)):
                        cursorCart.execute(sql,(oid+1,uid,str(date.today()).replace('-',''),input[i].get('productid'),input[i].get('amount')))
                        cursorCart.execute(sqlrem,uid)
                        cursorCart.execute(sqlremstock,(input[i].get('amount'),input[i].get('productid')))
                        cartCon.commit()
                    return render_template("cart.html", headings=heading,data=result)

                else:
                    for i in range(len(input)):
                        sql= "SELECT brand,model,price FROM tv WHERE productid = %s"
                        cursorCart.execute(sql,input[i].get('productid'))
                        temp=cursorCart.fetchall()
                        if temp == ():
                            return render_template("cart.html")
                        temp[0].update(input[i].items())
                        result=result+temp
                        cursorCart.commit()
                    return render_template("cart.html", headings=heading,data=result)


