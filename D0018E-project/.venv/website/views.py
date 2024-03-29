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
            sql = "SELECT productid,model, brand, size, resolution, price, stock FROM tv WHERE active=1"
            sqlAllRev="SELECT rating FROM reviews WHERE productid=%s"
            cursor.execute(sql)
            result = cursor.fetchall()
            for product in result:#for all products
                cursor.execute(sqlAllRev,product.get("productid"))
                temp = cursor.fetchall()
                if temp == ():#if no ratings
                    product["rating"]="-"
                    continue
                ratingvalue=0
                i=0
                for rating in temp: #sum of all ratings of product
                    ratingvalue+=rating.get("rating")
                    i+=1#number of ratings
                average=ratingvalue/i#average
                product["rating"]=average#add to product

    headings = ['Brand', 'Model', 'Size', 'Resolution', 'Price','Rating of 5', 'Stock']
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
    headings = ['Brand', 'Model', 'Size', 'Resolution', 'Price','Rating of 5', 'Stock']
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
                    homeConnection.commit()
                    
                else:
                    sqlGet = "INSERT INTO cart (id, productid, userid, amount) VALUES (1, %s, %s, %s)"
                    homeCursor.execute(sqlGet,(pid.get('productid'),uid[0].get('id'),amount))

                
                sql = "SELECT productid,model, brand, size, resolution, price, stock FROM tv where active = 1"
                sqlAllRev="SELECT rating FROM reviews WHERE productid=%s"
                homeCursor.execute(sql)
                result = homeCursor.fetchall()
                for product in result:#for all products
                    homeCursor.execute(sqlAllRev,product.get("productid"))
                    temp = homeCursor.fetchall()
                    if temp == ():#if no ratings
                        product["rating"]="-"
                        continue
                    ratingvalue=0
                    i=0
                    for rating in temp: #sum of all ratings of product
                        ratingvalue+=rating.get("rating")
                        i+=1#number of ratings
                    average=ratingvalue/i#average
                    product["rating"]=average#add to product

                homeConnection.commit()
                return render_template('index.html',headings=headings, data=result, value=login, form=form)
            elif(product is not None):
                
                return render_template("product.html",data = pid,form=form)
            else:
                return render_template('index.html',headings=headings, data=result, value=login, form=form)


@views.route('/product', methods=["GET", "POST"])
def product():
    form = addForm()
    homeConnection = connection()
    headings = ['Name', 'Rating', 'Comment']
    login=1
    if not session.get("name"):
        login=0
    print(login)
    rating = request.form.get("NUMBER")
    comment = request.form.get("comment")
    serial = request.form.get("model")
    sqlrev = "SELECT * FROM reviews WHERE productid = %s"
    if request.method == "GET":
        return render_template('product.html',headings=headings,title=title, data=reviewlist, value=login, form=form)
    if request.method == "POST":

        if(request.form["product"]=="add"):
            with homeConnection.cursor() as homeCursor:
                    pid = session["serial"]
                    sqlInsertRev="INSERT INTO reviews (userid,rating,comment,productid) VALUES (%s,%s,%s,%s)"
                    sqlUpdateRev="UPDATE reviews SET rating=%s, comment=%s WHERE userid=%s AND productid=%s"
                    sqlModel="SELECT model,brand FROM tv WHERE productid=%s"
                    sqlName="SELECT name FROM users WHERE id=%s"
                    sqlrev = "SELECT * FROM reviews WHERE productid = %s"
                    sqlGetUID="SELECT id FROM users WHERE mail=%s"
                    homeCursor.execute(sqlGetUID,session["name"])
                    uid=homeCursor.fetchall()
                    uid=uid[0].get("id")
                    homeCursor.execute(sqlrev,pid)
                    reviews=homeCursor.fetchall()
                    reviewlist=[]
                    existing=False
                    for review in reviews:
                        if(review.get('userid'))==uid:
                            existing=True
                        homeCursor.execute(sqlName,review.get('userid'))
                        name=homeCursor.fetchall()
                        name[0].update(review)
                        reviewlist=reviewlist+name
                    if existing==False:
                        homeCursor.execute(sqlInsertRev,(uid,rating,comment,pid))
                    else:
                        homeCursor.execute(sqlUpdateRev,(rating,comment,uid,pid))
                    homeCursor.execute(sqlModel,pid)
                    model=homeCursor.fetchall()
                    title=model[0].get("brand")
                    title=title+" "+model[0].get("model")
                    homeCursor.execute(sqlModel,pid)
                    model=homeCursor.fetchall()
                    title=model[0].get("brand")
                    title=title+" "+model[0].get("model")
                    homeConnection.commit()
                    return render_template('product.html',headings=headings, data=reviewlist, value=login, form=form, title=title)
        elif(request.form["product"]=="redirect"):
             with homeConnection:
                with homeConnection.cursor() as homeCursor:
                    sql = "SELECT productid FROM tv WHERE model = %s"
                    homeCursor.execute(sql,serial)
                    productid = homeCursor.fetchone()
                    pid = productid.get("productid")
                    sqlModel="SELECT model,brand FROM tv WHERE productid=%s"
                    sqlName="SELECT name FROM users WHERE id=%s"
                    sqlrev = "SELECT * FROM reviews WHERE productid = %s"
                    print(pid)
                    homeCursor.execute(sqlrev,pid)
                    reviews=homeCursor.fetchall()
                    reviewlist=[]
                    for review in reviews:
                        homeCursor.execute(sqlName,review.get('userid'))
                        name=homeCursor.fetchall()
                        name[0].update(review)
                        reviewlist=reviewlist+name
                    homeCursor.execute(sqlModel,pid)
                    model=homeCursor.fetchall()
                    title=model[0].get("brand")
                    title=title+" "+model[0].get("model")
                    homeCursor.execute(sqlModel,pid)
                    model=homeCursor.fetchall()
                    title=model[0].get("brand")
                    title=title+" "+model[0].get("model")
                    homeConnection.commit()
                    session["serial"] = pid
                    print(session["serial"])
                    return render_template('product.html',headings=headings,data=reviewlist, value=login, form=form,title=title)
        else:
            return render_template("index.html",headings=headings,data=reviewlist, value=login, form=form)
        
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
    


