from flask import Blueprint, render_template, request, redirect, session, Response
from website.classes import searchForm
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
    print(login)
    return render_template(
        'index.html',
        headings=headings,
        data=result,
        form = form
    )

@views.route("/search", methods = ["POST"])
def search():
    form = searchForm()
    c = connection()
    headings = ['Model', 'Brand', 'Size', 'Resolution', 'Price']


    if form.validate_on_submit():
        searches = form.searched.data
        with c:
            with c.cursor() as cursors:
                sql = "Select * FROM tv WHERE Brand Like %s;"
                print(sql)
                print(searches)
                cursors.execute(sql,searches)
                result = cursors.fetchall()
                print(result)
                return render_template("index.html", form = form, headings= headings, data = result)
    else:
        return render_template("search.html" , form = form)

