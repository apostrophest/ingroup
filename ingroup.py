import sys
import os
if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), 'project'))

from flask import Flask, render_template, request
import forums
import users
import threads
import posts
import prefs
import database

app = database.create_app()
app.config.from_object(prefs.Config)
app.test_request_context().push()

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


@app.route("/static/css/<css_file>")
def css_dir(css_file):
    pass


@app.route("/static/js/<js_file>")
def js_dir(js_file):
    pass


@app.route("/static/img/smilies/<image_name>")
def smilies_dir(image_name):
    pass


@app.route("/static/img/avatars/<image_name>")
def avatars_dir(image_name):
    pass


@app.route("/static/uploads/<file_name>")
def uploads_dir(file_name):
    pass


if __name__ == '__main__':
    app.run()
