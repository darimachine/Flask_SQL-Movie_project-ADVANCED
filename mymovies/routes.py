from flask import render_template, redirect, url_for, request
from mymovies.Tables_db import Movie
from mymovies.Forms import AddForm,EditForm
from mymovies import *
import requests
@app.route("/")
def home():
    movie_lengt=len(Movie.query.all())
    sorted_movies=Movie.query.order_by(Movie.rating).all()
    for movie in sorted_movies:
        movie.ranking=movie_lengt
        movie_lengt-=1
    db.session.commit()
    for i in Movie.query.all():
        print(i.title)
    return render_template("index.html",movies=sorted_movies)

@app.route("/edit",methods=["GET","POST"])
def update():
    editform = EditForm()
    movie_id = request.args.get('id')
    curent_movie =Movie.query.get(movie_id)
    if request.method == "POST":
        if editform.validate_on_submit():
            new_rating = float(editform.rating.data)
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
            parameters = {
                'api_key': API_KEY,
                'query': movie_title
            }
            response = requests.get(url="https://api.themoviedb.org/3/search/movie", params=parameters)
            response.raise_for_status()
            data = response.json()
            # for i in data['results']:
            #     print(i)
            return render_template('select.html',all_data=data['results'])
    return render_template('add.html',form=addform)
@app.route('/select')
def select():
    parameters={
        'api_key':API_KEY
    }
    movie_id = request.args.get('movie_id')

    response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", params=parameters)
    response.raise_for_status()
    data = response.json()
    print(1)
    print(data)
    title = data['title']
    img_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    year = data['release_date'][0:4]
    description = data['overview']
    new_movie=Movie(title=title,img_url=img_url,year=year,description=description)
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('update',id=new_movie.id))