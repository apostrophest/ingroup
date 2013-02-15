from flask import render_template, redirect, request, flash, url_for
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Markup

import pytz

from database import db, create_flask_app

app = create_flask_app()
login_manager = LoginManager()
login_manager.init_app(app)

from controllers import threads, posts, users

login_manager.token_loader(users.token_loader)
login_manager.user_loader(users.user_loader)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'


@app.route("/", defaults={'page': 1}, methods=['POST', 'GET'])
@app.route("/<int:page>", methods=['POST', 'GET'])
@login_required
def thread_list_view(page):
    if request.method == 'GET':
        thread_list = threads.thread_list(db.session, page=page)
        return render_template('thread_list.html', threads=thread_list)
    elif request.method == 'POST':
        new_thread = threads.create_thread(db.session, request.form['post-thread-title'])
        new_post = posts.make_post(db.session, current_user, new_thread, request.form['post-thread-content'])
        db.session.commit()
        return redirect(url_for('thread_view', thread_id=new_thread.id, _anchor=new_post.number))


@app.route("/thread/<int:thread_id>", methods=['POST', 'GET'])
@login_required
def thread_view(thread_id):
    if request.method == 'GET':
        posts_list = posts.post_list(db.session, thread_id)
        thread = threads.thread_from_id(db.session, thread_id)
        return render_template('thread_view.html', posts=posts_list, thread=thread, Markup=Markup, user_tz=pytz.timezone(current_user.timezone))
    elif request.method == 'POST':
        thread = threads.thread_from_id(db.session, thread_id)
        new_post = posts.make_post(db.session, current_user, thread, request.form['post-body'])
        db.session.commit()
        return redirect(url_for('thread_view', thread_id=thread.id, _anchor=new_post.number))


@app.route('/user/<int:uid>', defaults={'uid': 0}, methods=['POST', 'GET'])
@login_required
def user_profile(uid):
    if not uid:
        uid = current_user.id
    user = users.user_loader(uid)
    if user is not None:
        if request.method == 'POST':
            user.timezone = request.form['profile-timezone']
            user.display_name = request.form['profile-displayname']
            db.session.commit()
        return render_template('profile.html', user=user, timezones=pytz.common_timezones)


@app.route('/applicants', methods=['GET', 'POST'])
@login_required
def applicants():
    applicants = users.get_applicants(db.session)
    if request.method == 'GET':
        return render_template('applicants.html', applicants=applicants)
    elif request.method == 'POST':
        if 'applicant-accept' in request.form:
            users.accept_applicant(db.session, int(request.form['applicant-accept']), current_user)
            return redirect(url_for('applicants'))
        elif 'applicant-reject' in request.form:
            users.reject_applicant(db.session, int(request.form['applicant-reject']))
            return redirect(url_for('applicants'))
        else:
            return redirect(url_for('user_profile'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if 'login-username' in request.form:
            user = users.valid_credentials(db.session, request.form['login-username'], request.form['login-password'])
            if user is not None:
                login_user(user, remember=True)
                return redirect(url_for('thread_list_view'))
            else:
                flash(u'Login failed')
                return redirect(url_for('login'))
        elif 'apply-username' in request.form:
            user = users.create_user(db.session, request.form['apply-username'], request.form['apply-password'], request.form['apply-email'], request.form['apply-reason'])
            if user is None:
                flash(u'Username "{0}" is already taken.'.format(request.form['apply-username']))
                return redirect(url_for('login'))
            else:
                flash(u'Your application has been sent.')
                return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('thread_list_view'))


if __name__ == '__main__':
    app.run()
