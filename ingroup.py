from flask import Flask, render_template, request

from models import forums, users, threads, posts
import prefs
import database

app = database.create_app()
app.config.from_object(prefs.Config)

@app.route("/")
def forum_list_view():
    forum_list = forums.forum_list()
    return render_template('forum_list.html', forums=forum_list)


@app.route("/<int:id>")
def thread_list_view(id):
    thread_list = threads.thread_list(id)
    return render_template('thread_list.html', threads=thread_list)


@app.route("/thread/<int:id>")
def thread_view(id):
    posts_list = posts.post_list(id)
    return render_template('thread_view.html', posts=posts_list)


@app.route("/setup.py")
def remote_setup_access():
    # Refuse to serve setup script remotely
    return render_template('error.html', type=404, message='')


if __name__ == '__main__':
    app.run()
