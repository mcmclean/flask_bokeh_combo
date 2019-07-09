#!/usr/bin/env python3

import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path

# UPLOAD_FOLDER = '/path/to/the/uploads'
UPLOAD_FOLDER = str(Path.cwd())
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    html_string = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename): # i.e. if all is well
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            if file.filename.rsplit('.', 1)[1].lower() == 'xlsx':
            	df = pd.read_excel(file)
            elif file.filename.rsplit('.', 1)[1].lower() == 'csv':
            	df = pd.read_csv(file)
            html_string = df.head().to_html()
            return redirect(request.url_for)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    {0}
    '''.format(html_string)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
	app.run(debug = True)