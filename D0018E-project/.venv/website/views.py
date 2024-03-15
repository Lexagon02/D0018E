from flask import Blueprint, render_template, request, redirect, session, Response
from website.classes import searchForm, addForm
from flask_session import Session
import pymysql.cursors
WTF_CSRF_ENABLED = False

views = Blueprint('views', __name__)





# Connect to the database
def connection():
    connection = pymysql.connect(host='database-1.c1uyikioggel.eu-north-1.rds.amazonaws.com',
                                 user='admin',
                                 password='LTU123456',
                                 database='database',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection



@views.route("/", methods = ["GET", "POST"])
def home():
    form = searchForm()
    c = connection()

    with c:

        with c.cursor() as cursor:
            # Read a single record
            sql = "SELECT model, brand, size, resolution, price, stock FROM tv WHERE active=1"
            cursor.execute(sql)
            result = cursor.fetchall()

    headings = ['Brand', 'Model', 'Size', 'Resolution', 'Price', 'Stock']
    if not session.get("name"):
        login=0
    else:
        login=1
        
    return render_template(
        "index.html",
        headings=headings,
        data=result,
        form = form,
        value = login
    )
@views.route('/index', methods=["GET", "POST"])
def index():
    form = addForm()
    homeConnection = connection()
    headings = ['Brand', 'Model', 'Size', 'Resolution', 'Price', 'Stock']
    if request.method == "POST":
        serial = request.form.get("model",1)
        amount = request.form.get("NUMBER")
        add = request.form.get("add")
        product = request.form.get("product")
    amount = request.form.get("NUMBER")

    if not session.get("name"):
        login=0
        return render_template("login.html")
    login=1
    mail=session.get("name")

    with homeConnection:
        with homeConnection.cursor() as homeCursor:
            
            sql = "SELECT id FROM users WHERE mail = %s"
            homeCursor.execute(sql,mail)
            uid = homeCursor.fetchall()
            
            sql = "SELECT productid FROM tv WHERE model = %s"
            homeCursor.execute(sql,serial)
            pid = homeCursor.fetchone()

            sql = "SELECT amount FROM cart WHERE userid = %s AND productid = %s"
            homeCursor.execute(sql,(uid[0].get("id"),pid.get("productid")))
            stockAmount = homeCursor.fetchall()
            if(add is not None):
                print("addddddd")
                if(stockAmount != ()):
                    sql = "SELECT amount FROM cart WHERE userid = %s AND productid = %s"
                    sql2 = "Select stock from tv where productid = %s"
                    homeCursor.execute(sql,(uid[0].get("id"),pid.get("productid")))
                    cart = homeCursor.fetchall()
                    homeCursor.execute(sql2,pid.get("productid"))
                    stock = homeCursor.fetchall()
                    sqlGet = "UPDATE cart SET amount = %s WHERE userid = %s AND productid = %s"
                    if(int(stock[0].get("stock")) >= (int(amount) + int(cart[0].get("amount")))):
                        homeCursor.execute(sqlGet,((int(stockAmount[0].get("amount"))+int(amount)),uid[0].get("id"),pid.get("productid")))
                    else:
                        homeCursor.execute(sqlGet,(int(stock[0].get("stock")),uid[0].get("id"),pid.get("productid")))
                        pass
                    #result = homeCursor.fetchall()
                    homeConnection.commit()
                    
                else:
                    sqlGet = "INSERT INTO cart (id, productid, userid, amount) VALUES (1, %s, %s, %s)"
                    homeCursor.execute(sqlGet,(pid.get('productid'),uid[0].get('id'),amount))
                
                sql = "SELECT model, brand, size, resolution, price, stock FROM tv where active = 1"
                homeCursor.execute(sql)
                result = homeCursor.fetchall()
                homeConnection.commit()
            elif(product is not None):
                print(pid)
                print("producttttttt")
                return render_template("register.html",data = pid,form=form)
    return render_template('index.html',headings=headings, data=result, value=login, form=form)

@views.route("/search", methods = ["POST"])
def search():
    form = searchForm()
    c = connection()
    headings = ['Brand', 'Model', 'Size', 'Resolution', 'Price','Stock']
    if not session.get("name"):
        login=0
    else:
        login=1
    mail=session.get("name")
    if form.validate_on_submit():
        searches = form.searched.data
        with c:
            with c.cursor() as cursors:
                sql = "Select * FROM tv WHERE brand LIKE ('%%' %s '%%') AND active=1 or model like ('%%' %s '%%') AND active=1 or size like ('%%' %s '%%') AND active=1 or price like ('%%' %s '%%') AND active=1;"
                
                print(sql)
                print(searches)
                cursors.execute(sql,(searches,searches,searches,searches))
                result = cursors.fetchall()
                print(result)
                c.commit()
                return render_template("index.html", form = form, headings= headings,value=login, data = result)
    else:
        r = home()
        c.commit()
        return r
        #return render_template("index.html" , form = form,headings= headings, data = result)
    
@views.route("/products", methods = ["POST"])
def products():
    print("-------------------")
    form = searchForm()
    homeConnection = connection()
    if request.method=="POST":
        print("-------------------")
    with homeConnection:
        with homeConnection.cursor() as productCursor:
            serial = request.form.get("model",1)
    return render_template('index.html', form=form)


