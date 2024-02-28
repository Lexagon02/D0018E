from flask import Blueprint, render_template, request, redirect, session, Response
from website.classes import searchForm, addForm
from flask_session import Session
import pymysql.cursors
WTF_CSRF_ENABLED = False

views = Blueprint('views', __name__)





# Connect to the database
def connection():
    connection = pymysql.connect(host='d0018e-database.cvwk6aiy4nnq.eu-north-1.rds.amazonaws.com',
                                 user='admin',
                                 password='ltu1234567',
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
            sql = "SELECT model, brand, size, resolution, price, stock FROM tv"
            cursor.execute(sql)
            result = cursor.fetchall()

    headings = ['Model', 'Brand', 'Size', 'Resolution', 'Price', 'Stock']
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
    headings = ['Model', 'Brand', 'Size', 'Resolution', 'Price', 'Stock']
    if request.method == "POST":
        serial = request.form.get("model",1)
        amount = request.form.get("NUMBER")
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
            pid = homeCursor.fetchall()
            sqlGet = "INSERT INTO cart (id, productid, userid, amount) VALUES (1, %s, %s, %s)"
            sql = "SELECT model, brand, size, resolution, price, stock FROM tv"
            homeCursor.execute(sql)
            result = homeCursor.fetchall()
            homeCursor.execute(sqlGet,(pid[0].get('productid'),uid[0].get('id'),amount))
            homeConnection.commit()
    return render_template('index.html',headings=headings, data=result, value=login, form=form)

@views.route("/search", methods = ["POST"])
def search():
    form = searchForm()
    c = connection()
    headings = ['Model', 'Brand', 'Size', 'Resolution', 'Price','Stock']


    if form.validate_on_submit():
        searches = form.searched.data
        with c:
            with c.cursor() as cursors:
                sql = "Select * FROM tv WHERE Brand Like (%% + %%s + %%);"
                print(sql)
                print(searches)
                cursors.execute(sql,searches)
                result = cursors.fetchall()
                print(result)
                return render_template("index.html", form = form, headings= headings, data = result)
    else:
        r = home()
        return r
        #return render_template("index.html" , form = form,headings= headings, data = result)

