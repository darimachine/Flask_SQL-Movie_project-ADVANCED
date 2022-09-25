from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///movie_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(40),default='default.jpg')
class EditForm(FlaskForm):
    rating = StringField("Your rating from 0.00 to 10.00",validators=[DataRequired()])
    review = StringField("Your review",validators=[DataRequired()])
    submit = SubmitField("Done")
class AddForm(FlaskForm):
    title = StringField("Movie Title",validators=[DataRequired()])
    submit = SubmitField("Add Movie")
db.create_all()

@app.route("/")
def home():
    for i in Movie.query.all():
        print(i.title)
    return render_template("index.html",movies=Movie.query.all())

@app.route("/edit",methods=["GET","POST"])
def update():
    editform = EditForm()
    movie_id = request.args.get('id')
    curent_movie =Movie.query.get(movie_id)
    if request.method == "POST":
        if editform.validate_on_submit():
            new_rating = editform.rating.data
            new_review = editform.review.data
            curent_movie.rating = new_rating
            curent_movie.review = new_review
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('edit.html', form=editform, movie=curent_movie)
@app.route("/delete",methods=["GET","POST"])
def delete():
    movie_id = request.args.get('id')
    curent_movie = Movie.query.get(movie_id)
    db.session.delete(curent_movie)
    db.session.commit()
    return redirect(url_for('home'))
@app.route("/add",methods=["GET","POST"])
def add():
    addform = AddForm()
    if request.method == "POST":
        if addform.validate_on_submit():
            movie_title = addform.title.data
            response = requests.get(url="http://api.open-notify.org/iss-now.json")
            response.raise_for_status()

            data = response.json()
    return render_template('add.html',form=addform)
if __name__ == '__main__':
    app.run(debug=True)
