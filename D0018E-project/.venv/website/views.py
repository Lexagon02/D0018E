from flask import Blueprint, render_template

views = Blueprint('views', __name__)

import pymysql.cursors

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
            sql = "SELECT model, brand, size, resolution, price FROM `tv`"
            cursor.execute(sql)
            result = cursor.fetchall()

    headings = ['Model', 'Brand', 'Size', 'Resolution', 'Price']

    return render_template(
        'index.html',
        headings=headings,
        data=result
    )
