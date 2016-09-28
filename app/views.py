from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required, login_user, logout_user, flash, current_user

from .forms import UploadForm, LoginForm, RegistrationForm
from .models import User
from app import app, db, lm, bcrypt
from upload import s3_upload


@lm.user_loader
def user_loader(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_page():
    user = g.user
    form = UploadForm()
    if form.validate_on_submit():
        output = s3_upload(form.upload_file)
        flash('{src} uploaded to S3 as {dst}'.format(src=form.upload_file.data.filename, dst=output))
    return render_template('upload.html',
                           form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    form = LoginForm()
    # if g.user is not None and g.user.is_authenticated:
    #     return redirect(url_for('upload_page'))
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session['remember_me'] = form.remember_me.data
                login_user(user, remember=True)
                next = request.args.get('next')
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                return redirect(next or url_for('upload_page'))
            else:
                flash('Invalid Password. Please try again')
        else:
            flash('We were unable to find a user for this email. Please register.')
            return redirect(url_for('register'))
    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        if User.query.filter_by(email = form.email.data).first():
            flash('You have already registered. Please login.')
            return redirect(url_for('login'))
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                    password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Thanks for registering')
        return redirect(url_for('upload_page'))
    return render_template('register.html', form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = g.user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect('/login')
