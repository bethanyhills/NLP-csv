from flask import Flask, render_template, flash, redirect
from app import app
from .forms import UploadForm
from upload import s3_upload

@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Beth'}
    return render_template('index.html', user=user)

@app.route('/upload', methods=['POST', 'GET'])
def upload_page():
    form = UploadForm()
    if form.validate_on_submit():
        output = s3_upload(form.upload_file)
        flash('{src} uploaded to S3 as {dst}'.format(src=form.upload_file.data.filename, dst=output))
    return render_template('upload.html', form=form)