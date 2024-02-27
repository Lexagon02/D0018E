from website import create_app
from flask_session import Session

app = create_app()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = "secret"
Session(app)

if __name__ == '__main__':
    app.run(debug=True)