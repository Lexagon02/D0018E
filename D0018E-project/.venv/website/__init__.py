from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    print("hej")

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
            sql = "SELECT *  FROM `users`"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)

    return app
