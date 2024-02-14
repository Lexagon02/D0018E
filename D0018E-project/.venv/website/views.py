from flask import Blueprint, render_template, request
import pymysql.cursors

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

    return render_template(
        'index.html',
        headings=headings,
        data=result
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
        with homeConnection:
            with homeConnection.cursor() as homeCursor:
                sqlGet = "INSERT INTO cart (id, productid, userid, amount) VALUES (1, %s, 1, %s)"
                sql = "SELECT model, brand, size, resolution, price, stock FROM tv"
                homeCursor.execute(sql)
                result = homeCursor.fetchall()
                homeCursor.execute(sqlGet,(serial,amount))
                homeConnection.commit()
                return render_template('index.html',headings=headings,data=result)
    return render_template('index.html',headings=headings, data=result)

