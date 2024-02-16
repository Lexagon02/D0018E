from flask import Blueprint, render_template, request,redirect, session
import pymysql.cursors
from flask_session import Session

views = Blueprint('views', __name__)


# Connect to the database



@views.route('/')

def home():
    connection = pymysql.connect(host='d0018e-database.cvwk6aiy4nnq.eu-north-1.rds.amazonaws.com',
                             user='admin',
                             password='ltu1234567',
                             database='database',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection:

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT model, brand, size, resolution, price, stock FROM tv"
            cursor.execute(sql)
            result = cursor.fetchall()

    headings = ['Model', 'Brand', 'Size', 'Resolution', 'Price', 'Stock']
    if not session.get("name"):
            login=0
    else:
        login=1
    print(login)
    return render_template(
        'index.html',
        headings=headings,
        data=result,
        value=login
    )

@views.route('/index', methods=["GET", "POST"])
def index():
    homeConnection = pymysql.connect(host='d0018e-database.cvwk6aiy4nnq.eu-north-1.rds.amazonaws.com',
                             user='admin',
                             password='ltu1234567',
                             database='database',
                             cursorclass=pymysql.cursors.DictCursor)
    

    headings = ['Model', 'Brand', 'Size', 'Resolution', 'Price', 'Stock']
    
    if request.method == "POST":
        serial = request.form.get("model",1)
        amount = request.form.get("NUMBER")
        print(serial)
        print(amount)
        print(session.get("name"))
        if not session.get("name"):
            login=0
            return render_template("login.html")
        login=1
        mail=session.get("name")
        print(login)
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
                return render_template('index.html',headings=headings,data=result)
    return render_template('index.html',headings=headings, data=result, value=login)

