from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class searchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

class addForm(FlaskForm):
    submit = SubmitField("Submit")
    submit2 = SubmitField("product") 
