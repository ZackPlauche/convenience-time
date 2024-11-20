import random

from flask import Flask, render_template, abort, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Episode

app = Flask(__name__)

engine = create_engine('sqlite:///episodes.db')
Session = sessionmaker(engine)


@app.route('/')
def home():
    with Session() as session:
        episodes = session.query(Episode).all()[::-1]
        return render_template('index.html', episodes=episodes)


@app.route('/watch/<int:pk>')
def watch_movie(pk):
    with Session() as session:
        episode = session.query(Episode).get(pk)
        episode.watched = True
        session.commit()
        if episode is None:
            abort(404)
        return redirect('/')


@app.route('/unwatch/<int:pk>')
def unwatch_movie(pk):
    with Session() as session:
        episode = session.query(Episode).get(pk)
        if episode is None:
            abort(404)
        else:
            episode.watched = False
            session.commit()
        return redirect('/')


@app.route('/watch/random')
def watch_random_episode():
    with Session() as session:
        episodes = session.query(Episode).filter_by(watched=False).all()
        if episodes:
            random_episode = random.choice(episodes)
            random_episode.watched = True
            session.commit()
            return redirect(random_episode.url)
        return redirect('/')



if __name__ == '__main__':
    app.run(debug=True, port=5000)
