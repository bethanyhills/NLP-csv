from flask import render_template, flash, redirect
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, flash, current_user
from flask.ext.bcrypt import Bcrypt

from .forms import UploadForm, LoginForm
from models import User
from app import app, db
from upload import s3_upload

# @app.route('/')
# @app.route('/index')
# def index():
#     user = {'name': 'Beth'}
#     return render_template('index.html', user=user)

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_page():
    form = UploadForm()
    if form.validate_on_submit():
        output = s3_upload(form.upload_file)
        flash('{src} uploaded to S3 as {dst}'.format(src=form.upload_file.data.filename, dst=output))
    return render_template('upload.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if (user.password == form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect('/upload')
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")