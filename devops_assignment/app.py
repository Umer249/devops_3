from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['blog_db']
posts_collection = db['posts']

@app.route('/')
def index():
    posts = list(posts_collection.find())
    return render_template('index.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            return 'Title is required!', 400

        posts_collection.insert_one({'title': title, 'content': content})
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = posts_collection.find_one({'_id': id})

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            return 'Title is required!', 400

        posts_collection.update_one({'_id': id}, {'$set': {'title': title, 'content': content}})
        return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    posts_collection.delete_one({'_id': id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 