from flask import (Flask, request, session, g, redirect, url_for, abort,
                  render_template, flash)
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
import subprocess
import sys
import argparse


# create the application
app = Flask(__name__)

# tell the app where our db is.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anonfeedback.db'

# set up the db through SQLAlchemy
db = SQLAlchemy(app)
db.init_app(app)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255))
    content = db.Column(db.String(16384))
    time_posted = db.Column(db.DateTime, default=datetime.datetime.now())


@app.route('/')
def home():
    posts = Post.query.all()
    posts = list(reversed(sorted(posts, key=lambda x: x.time_posted)))
    for post in posts:
        post.time_posted = post.time_posted.strftime("%b %d, %Y at %H:%M")

    return render_template('home.html', posts=posts)


@app.route('/feedback/', methods=['GET', 'POST'])
def give_feedback(term=None):
    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']

        post = Post(subject=subject, content=content)
        db.session.add(post)
        db.session.commit()

        return redirect('/')

    return render_template('feedback.html')


if __name__ == '__main__':
    sys.dont_write_bytecode = True

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="listen to this IP address",
                        default="127.0.0.1")
    parser.add_argument("-p", "--port", help="listen to this port",
                        default="5000", type=int)
    parser.add_argument("-d", "--debug", help="turn debugging on",
                        action="store_true")

    args = parser.parse_args()

    app.run(args.ip, args.port, args.debug)
