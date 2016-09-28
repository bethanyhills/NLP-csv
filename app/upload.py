from app import app
from flask import g
import boto
from boto.s3.key import Key

def s3_upload(file):
    '''Uploads a file to s3 in the appropriate s3 bucket'''
    s3_connection = boto.connect_s3(
        aws_access_key_id=app.config["S3_KEY"],
        aws_secret_access_key=app.config["S3_SECRET"],
        calling_format='boto.s3.connection.OrdinaryCallingFormat',
    )
    bucket = s3_connection.get_bucket(app.config["S3_BUCKET"])
    filename = file.data.filename
    k = Key(bucket)
    user = g.user
    #in the future, separate user imports by using their userID instead of putting all in 'imports'
    k.key = '/imports/' + str(user.id) + '/' + file.data.filename
    k.set_contents_from_string(file.data.read())
    k.set_acl('public-read')

    return filename