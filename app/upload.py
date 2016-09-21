import os
import boto
from boto.s3.key import Key

def s3_upload(file):
    '''Uploads a file to s3 in the appropriate s3 bucket'''
    s3_connection = boto.connect_s3(
        aws_access_key_id=os.environ["S3_KEY"],
        aws_secret_access_key=os.environ["S3_SECRET"],
        calling_format='boto.s3.connection.OrdinaryCallingFormat',
    )
    bucket = s3_connection.get_bucket(os.environ["S3_BUCKET"])
    filename = file.data.filename
    k = Key(bucket)

    #in the future, separate user imports by using their userID instead of putting all in 'imports'
    k.key = '/imports/' + file.data.filename
    k.set_contents_from_string(file.data.read())
    k.set_acl('public-read')

    return filename