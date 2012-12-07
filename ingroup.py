from flask import render_template
from database import db, create_flask_app

app = create_flask_app()

from controllers import forums, threads, posts

@app.route("/")
def forum_list_view():
    forum_list = forums.forum_list(db.session)
    return render_template('forum_list.html', forums=forum_list)


@app.route("/<int:id>")
def thread_list_view(id):
    thread_list = threads.thread_list(db.session, id)
    return render_template('thread_list.html', threads=thread_list)


@app.route("/thread/<int:id>")
def thread_view(id):
    posts_list = posts.post_list(db.session, id)
    thread = threads.thread_from_id(db.session, id)
    return render_template('thread_view.html', posts=posts_list, thread=thread)


@app.route("/setup.py")
def remote_setup_access():
    # Refuse to serve setup script remotely
    return render_template('error.html', type=404, message='')


if __name__ == '__main__':
    app.run()
