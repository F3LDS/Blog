#!env/bin/python
import sys
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from pymongo import MongoClient


client = MongoClient('mongodb://alex:ww@ds027668.mongolab.com:27668/refractix')
db = client['refractix']
assignmentdb = db['assignmentdb']


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'static/content'
POST_DIR = 'posts'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/posts/")
def posts():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=False)
    firstpost = posts[0]
    return render_template('posts.html', posts=posts, firstpost=firstpost)

@app.route("/posts/archive/")
def archive():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=False)
    return render_template('archive.html', posts=posts)

@app.route('/posts/<name>/')
def post(name):
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post, posts=posts)

@app.route('/school/')
def school():
    assignments = assignmentdb.find()
    #for assignments = assignmentdb.find({"class"})
    #print assignments
    #return render_template('school.html', assignments=assignments)




if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='localhost', debug=True)
