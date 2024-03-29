from flask import Blueprint, render_template, request, redirect, session
from flask_session import Session
from datetime import date
import pymysql.cursors
def connection():
    connection = pymysql.connect(host='database-1.c1uyikioggel.eu-north-1.rds.amazonaws.com',
                                 user='admin',
                                 password='LTU123456',
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
            sql= "SELECT * FROM users where mail = %s"
            cursors.execute(sql,mail)
            result = cursors.fetchall()
            print(result)
            print(len(result))
            if(len(result)==0):
            # Read a single record
                print("-------")
                sql = "INSERT INTO users (name,surname,mail,password,address,isAdmin) VALUES (%s,%s,%s,%s,%s,0);"
                cursors.execute(sql,(first_name,surname,mail,password,address))
                print("here")
                sql = "SELECT name,surname,password,address,isAdmin FROM users WHERE mail = %s AND password = %s"
                cursors.execute(sql,(mail,password))
                result = cursors.fetchall()
                registerCon.commit() 
                return render_template("profile.html", data=result)
            else:
                pass
                registerCon.commit() 
            
       
       
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
                sql = "SELECT name,surname,password,address,isAdmin FROM users WHERE mail = %s AND password = %s"
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
            sqluser="SELECT * FROM users WHERE mail=%s"
            if request.method == "GET":
                cursorp.execute(sqluser,session["name"])
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
                header=["name","surname","password","address"]
                print(address)
                data=[first_name,surname,password,address]
                sql = "UPDATE users SET {} = %s WHERE mail = %s"

                for i in range(4):
                    if data[i] != '':
                        # Constructing the SET clause dynamically
                        set_clause = header[i]
                        # Using placeholders for column names without single quotes
                        cursorp.execute(sql.format(set_clause), (data[i], session["name"]))
                
                cursorp.execute(sqluser,session["name"])
                result=cursorp.fetchall()
                isAdmin=result[0].get('isAdmin')
                profileCon.commit()
                return render_template("profile.html",isAdmin=isAdmin,data=result)

@auth.route("/adminStuff", methods = ["GET", "POST"])
def adminStuff():
    adminCon=connection()
    heading = ['Brand', 'Model', 'Size', 'Resolution', 'Price', "Stock",'ProductID']


    #SQL statments for the page
    sqlTV =  "SELECT model, brand, size, resolution, price, productid,stock FROM `tv` WHERE active = 1"
    sqlUser =  "SELECT name, surname, mail, password, address, isAdmin FROM `users`"
    sqlOrder =  "SELECT userid,orderid,date FROM `orders` GROUP BY orderid ORDER BY orderid"
    sqlGetModel="SELECT model,brand FROM tv WHERE productid=%s"
    sqlOrderUser =  "SELECT name, surname, mail, address FROM users WHERE id=%s"
    sqlReviewMail="SELECT mail FROM users WHERE id=%s"

    if request.method == "POST":
        if request.form["action"]=="AddTV":
            model = request.form.get("model")
            brand = request.form.get("brand")
            size = request.form.get("size")
            res = request.form.get("res")
            price = request.form.get("price")
            stock = request.form.get("stock") 
            pid = request.form.get("pid") 
    
            with adminCon:
                with adminCon.cursor() as cursoraddTV:
                    # Read a single record
                    sql1 = "INSERT INTO tv (model,brand,size,resolution,price,stock) VALUES (%s,%s,%s,%s,%s,%s);"
                    if not pid:
                        cursoraddTV.execute(sql1,(model,brand,size,res,price,stock))

                    else:
                        sql = "UPDATE tv SET {} = %s WHERE productid = %s"
                        header=["brand","model","size","resolution","price","stock"]
                        data=[brand,model,size,res,price,stock]
                        for i in range(6):
                            if not data[i] :
                                continue
                            set_clause = header[i]
                            print(set_clause)
                            print(data[i])
                            # Using placeholders for column names without single quotes
                            cursoraddTV.execute(sql.format(set_clause), (data[i], pid))

                    #Load all data for all tables on page
                    cursoraddTV.execute(sqlTV)
                    result = cursoraddTV.fetchall()
                    cursoraddTV.execute(sqlUser)
                    userdata= cursoraddTV.fetchall()
                    cursoraddTV.execute(sqlOrder)
                    orderdata = cursoraddTV.fetchall()
                    orderresult=[]
                    for order in orderdata:#Combine orderdata with userdata
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
                    sqlDelTv = "UPDATE tv SET active=0 WHERE model=%s"
                    cursorRemTV.execute(sqlDelTv,(model))
                    
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
            mail = request.form.get("mailRem")
            with adminRemUser:
                with adminRemUser.cursor() as cursorRemUser:
                    sql3 = "DELETE FROM users WHERE mail=%s;"
                    sqlDelORder="DELETE FROM orders WHERE userid=%s"
                    sqlUserID="SELECT id FROM users WHERE mail=%s"
                    sqlDelCart="DELETE FROM cart WHERE userid=%s"
                    sqlDelReviews="DELETE FROM reviews WHERE userid=%s"
                    cursorRemUser.execute(sqlUserID,mail)#get id from mail
                    user=cursorRemUser.fetchall()
                    
                    
                    #Load in all fields on adminpage
                    cursorRemUser.execute(sqlTV)
                    result = cursorRemUser.fetchall()
                    
                    cursorRemUser.execute(sqlOrder)
                    orderdata = cursorRemUser.fetchall()
                    orderresult=[]
                    for order in orderdata:
                        cursorRemUser.execute(sqlOrderUser,order.get('userid'))
                        temp=cursorRemUser.fetchall()
                        temp[0].update(order)
                        orderresult=orderresult+temp
                    
                    if(user==()):
                        return
                    print("a")
                    cursorRemUser.execute(sqlDelORder,user[0].get('id'))#delete orders by user
                    cursorRemUser.execute(sqlDelCart,user[0].get('id'))#delete users cart
                    cursorRemUser.execute(sqlDelReviews,user[0].get('id'))
                    cursorRemUser.execute(sql3,(mail))#delete user
                    
                    cursorRemUser.execute(sqlUser)
                    userdata = cursorRemUser.fetchall()

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
        if request.form["action"]=="CheckOrder":
            adminRemUser=connection()
            order = request.form.get("orderCheck")
            with adminRemUser:
                with adminRemUser.cursor() as cursorRemUser:
                    sql3 = "SELECT * FROM orders WHERE orderid=%s;"
                    cursorRemUser.execute(sql3,(order))
                    checkorderdata=cursorRemUser.fetchall()
                    checkorderresult=[]
                    for order in checkorderdata:
                        cursorRemUser.execute(sqlOrderUser,order.get('userid'))
                        temp=cursorRemUser.fetchall()
                        temp[0].update(order)
                        cursorRemUser.execute(sqlGetModel,order.get('productid'))
                        temp2=cursorRemUser.fetchall()
                        temp2[0].update(temp[0])
                        checkorderresult=checkorderresult+temp2
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
            return render_template("adminStuff.html",headings=heading,data=result,userdata=userdata,orderdata=orderresult,checkorderdata=checkorderresult) 
        if request.form["action"]=="DeleteReview":
            adminRemReview=connection()
            uid = request.form.get("reviewRem")
            print("rem")
            with adminRemReview:
                with adminRemReview.cursor() as cursorRemReview:
                    sql3 = "DELETE FROM reviews WHERE userid=%s and productid=%s;"
                    sql6 = "SELECT * FROM reviews WHERE productid=%s;"
                    if not session.get("pid"):
                        pid=0
                    else:
                        pid=session["pid"]
                    cursorRemReview.execute(sql3,(uid,pid))
                    cursorRemReview.execute(sqlTV)
                    result = cursorRemReview.fetchall()
                    cursorRemReview.execute(sqlUser)
                    userdata = cursorRemReview.fetchall()
                    cursorRemReview.execute(sqlOrder)
                    orderdata = cursorRemReview.fetchall()
                    orderresult=[]
                    for order in orderdata:
                        cursorRemReview.execute(sqlOrderUser,order.get('userid'))
                        temp=cursorRemReview.fetchall()
                        temp[0].update(order)
                        orderresult=orderresult+temp
                    cursorRemReview.execute(sql6,(pid))
                    reviewdata = cursorRemReview.fetchall()
                    reviewresult=[]
                    for review in reviewdata:
                        cursorRemReview.execute(sqlReviewMail,review.get('userid'))
                        temp=cursorRemReview.fetchall()
                        temp[0].update(review)
                        reviewresult=reviewresult+temp
                    adminRemReview.commit()
                    return render_template("adminStuff.html",headings=heading,data=result,userdata=userdata,orderdata=orderresult,reviewresult=reviewresult)
        if request.form["action"]=="searchReview":
            adminRemReview=connection()
            model = request.form.get("searchRev")
            with adminRemReview:
                with adminRemReview.cursor() as cursorRemReview:
                    sql3 = "SELECT * FROM reviews WHERE productid=%s;"
                    sql4 = "SELECT productid FROM tv WHERE model=%s;"
                    cursorRemReview.execute(sql4,(model))
                    pid=cursorRemReview.fetchall()
                    print(pid)
                    cursorRemReview.execute(sqlTV)
                    result = cursorRemReview.fetchall()
                    cursorRemReview.execute(sqlUser)
                    userdata = cursorRemReview.fetchall()
                    cursorRemReview.execute(sqlOrder)
                    orderdata = cursorRemReview.fetchall()

                    orderresult=[]
                    for order in orderdata:
                        cursorRemReview.execute(sqlOrderUser,order.get('userid'))
                        temp=cursorRemReview.fetchall()
                        temp[0].update(order)
                        orderresult=orderresult+temp
                    if pid==():
                        print("p")
                    else:
                        pid=pid[0].get("productid")
                        session["pid"]=pid
                       
                        cursorRemReview.execute(sql3,(pid))
                        reviewdata=cursorRemReview.fetchall()
                        reviewresult=[]
                        for review in reviewdata:
                            cursorRemReview.execute(sqlReviewMail,review.get('userid'))
                            temp=cursorRemReview.fetchall()
                            temp[0].update(review)
                            reviewresult=reviewresult+temp
                        adminRemReview.commit()
                        return render_template("adminStuff.html",headings=heading,data=result,userdata=userdata,orderdata=orderresult,reviewresult=reviewresult)
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
                    sqlStock="SELECT stock,active FROM tv WHERE productid =%s"
                    sql = "INSERT INTO orders (orderid,userid,date,productid,amount) VALUES(%s,%s,%s,%s,%s)"
                    sqlrem="DELETE FROM cart WHERE userid=%s"
                    sqlremstock="UPDATE tv SET stock=stock-%s WHERE productid=%s AND stock>0"
                    for i in range(len(input)):
                        cursorCart.execute(sqlStock,(input[i].get('productid')))
                        stock=cursorCart.fetchall()
                        if(stock[0].get('stock')>=input[i].get('amount') and stock[0].get('active')==1):
                            cursorCart.execute(sql,(oid+1,uid,str(date.today()).replace('-',''),input[i].get('productid'),input[i].get('amount')))
                            cursorCart.execute(sqlremstock,(input[i].get('amount'),input[i].get('productid')))
                    cursorCart.execute(sqlrem,uid)
                    cartCon.commit()
                    return render_template("cart.html", headings=heading,data=result)

                else:
                    for i in range(len(input)):
                        sql= "SELECT brand,model,price FROM tv WHERE productid = %s AND active=1"
                        cursorCart.execute(sql,(input[i].get('productid')))
                        temp=cursorCart.fetchall()
                        if temp == ():
                            return render_template("cart.html")
                        temp[0].update(input[i].items())
                        result=result+temp
                        cartCon.commit()
                    return render_template("cart.html", headings=heading,data=result)
                
