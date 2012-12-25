from flask import render_template, redirect, request, flash, url_for
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user

from database import db, create_flask_app

app = create_flask_app()
login_manager = LoginManager()
login_manager.init_app(app)

from controllers import forums, threads, posts, users

login_manager.token_loader(users.token_loader)
login_manager.user_loader(users.user_loader)
login_manager.login_view = 'forum_list_view'
login_manager.session_protection = 'strong'


@app.route("/", methods=['POST', 'GET'])
def forum_list_view():
    if request.method == 'GET':
        if current_user.is_authenticated():
            forum_list = forums.forum_list(db.session)
            return render_template('forum_list.html', forums=forum_list)
        else:
            return redirect('/login')
    el
@app.route("/<int:forum_id>")
@login_required
def thread_list_view(forum_id):
    thread_list = threads.thread_list(db.session, forum_id)
    return render_template('thread_list.html', threads=thread_list)


@app.route("/thread/<int:thread_id>", methods=['POST', 'GET'])
@login_required
def thread_view(thread_id):
    if request.method == 'GET':
        posts_list = posts.post_list(db.session, thread_id)
        thread = threads.thread_from_id(db.session, thread_id)
        return render_template('thread_view.html', posts=posts_list, thread=thread)
    elif request.method == 'POST':
        post = posts.make_post(db.session, current_user, thread_id, request.form['post-body'])
        return redirect(url_for('/thread/{0:>d}'.format(thread_id), _anchor=post.id))


@app.route("/setup.py")
def remote_setup_access():
    # Refuse to serve setup script remotely
    return render_template('error.html', type=404, message='')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if 'login-username' in request.form:
            user = users.valid_credentials(db.session, request.form['login-username'], request.form['login-password'])
            if user is not None:
                login_user(user, remember=False)
                return redirect('/')
            else:
                flash(u'Login failed')
                return redirect('/login')
        elif 'apply-username' in request.form:
            user = users.create_user(db.session, request.form['apply-username'], request.form['apply-password'], request.form['apply-email'], request.form['apply-reason'])
            if user is None:
                flash(u'Username "%s" is already taken.' % request.form['apply-username'])
                return redirect('/login')
            else:
                flash(u'Your application has been sent.')
                return redirect('/login')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run()
