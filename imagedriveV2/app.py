from flask import Flask, request, redirect, render_template, send_file, url_for
import boto3
import io
import os
from datetime import datetime

app = Flask(__name__)

# Ceph RGW S3 config
s3 = boto3.client(
    's3',
    endpoint_url='http://10.0.2.15:80',
    aws_access_key_id='foo',
    aws_secret_access_key='bar',
    region_name='us-east-1'
)

BUCKET = 'imagedrive'

@app.route('/')
def index():
    objects = s3.list_objects_v2(Bucket=BUCKET).get('Contents', [])
    # Sort by LastModified time, newest first
    objects = sorted(objects, key=lambda x: x['LastModified'], reverse=True)
    return render_template('index.html', objects=objects)

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    for file in files:
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            s3.upload_fileobj(file, BUCKET, file.filename)
    return redirect(url_for('index'))

@app.route('/view/<filename>')
def view_image(filename):
    img = s3.get_object(Bucket=BUCKET, Key=filename)
    return send_file(
        io.BytesIO(img['Body'].read()),
        mimetype='image/jpeg',  # can improve later to auto-detect
        download_name=filename
    )

@app.route('/delete/<filename>', methods=['POST'])
def delete_image(filename):
    s3.delete_object(Bucket=BUCKET, Key=filename)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
