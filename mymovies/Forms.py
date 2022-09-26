from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class EditForm(FlaskForm):
    rating = StringField("Your rating from 0.00 to 10.00",validators=[DataRequired()])
    review = StringField("Your review",validators=[DataRequired()])
    submit = SubmitField("Done")
class AddForm(FlaskForm):
    title = StringField("Movie Title",validators=[DataRequired()])
    submit = SubmitField("Add Movie")