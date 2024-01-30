from flask import Blueprint, render_template

views = Blueprint('views', __name__)

import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='d0018e-database.cvwk6aiy4nnq.eu-north-1.rds.amazonaws.com',
                             user='admin',
                             password='ltu1234567',
                             database='database',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT *  FROM `tv`"
        cursor.execute(sql)
        result = cursor.fetchall()

@views.route('/')
def home():
    return render_template("index.html", data=result)
