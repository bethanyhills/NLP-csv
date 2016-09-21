from flask import Flask, render_template, flash, redirect
from app import app
from .forms import UploadForm

@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Beth'}
    return render_template('index.html', user=user)

@app.route('/upload', methods=['POST', 'GET'])
def upload_page():
    form = UploadForm()
    if form.validate_on_submit():
        output = form.upload_file
        flash('{src} uploaded to S3'.format(src=form.upload_file.data.filename))
    return render_template('upload.html', form=form)