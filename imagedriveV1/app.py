from flask import Flask, request, redirect, render_template, send_file
import boto3
import io
import os

app = Flask(__name__)

# Ceph RGW credentials
s3 = boto3.client(
    's3',
    endpoint_url='http://10.0.2.15:80',  # your RGW endpoint
    aws_access_key_id='foo',
    aws_secret_access_key='bar',
    region_name='us-east-1'
)
BUCKET = 'mybucket'

@app.route('/')
def index():
    objects = s3.list_objects_v2(Bucket=BUCKET).get('Contents', [])
    return render_template('index.html', objects=objects)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        s3.upload_fileobj(file, BUCKET, file.filename)
    return redirect('/')

@app.route('/view/<filename>')
def view_image(filename):
    img = s3.get_object(Bucket=BUCKET, Key=filename)
    return send_file(
        io.BytesIO(img['Body'].read()),
        mimetype='image/jpeg',  # or detect dynamically
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True)
