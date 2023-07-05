# from flask import Flask
# app = Flask(__name__)
#
# @app.route("/")
# def hello():
#   return "Hello World!"
#
# if __name__ == "__main__":
#   app.run()

from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import urllib.request

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def myhome():
    return render_template('home.html')


@app.route('/algo1')
def algo1():
    return render_template('algo1.html')


@app.route('/algo2')
def algo2():
    return render_template('algo2.html')


@app.route('/algo3')
def algo3():
    return render_template('algo3.html')


@app.route('/algo4')
def algo4():
    return render_template('algo4.html')


@app.route('/forms', methods=['GET', 'POST'])
def forms():
    return render_template('forms.html')


@app.route('/process_forms', methods=['POST'])
def process_forms():
    input1 = request.form['input1']
    input2 = request.form['input2']
    input3 = request.form['input3']

    # Process the inputs using your algorithm
    # ...
    print("input1: " + input1, "input2: " + input2, "input 3: " + input3)
    return "Inputs processed successfully."

#
# @app.route('/', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     files = request.files.getlist('file')
#     if len(files) > 2:
#         error = "You are only allowed to upload a maximum of 2 files"
#         flash(error)
#         return render_template("upload.html")
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file_names.append(filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         else:
#             flash('Allowed image types are -> png, jpg, jpeg, gif')
#             return redirect(request.url)
#
#     return render_template('upload.html', filenames=file_names)





def upload_image(page):
    file_names = []
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('file')
    if len(files) != 2:
        flash("You are only allowed to upload 2 files")
        return render_template(page)
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template(page, filenames=file_names[:2])


@app.route('/algo1', methods=['POST'])
def upload_image_algo1():
    return upload_image("algo1.html")


@app.route('/algo2', methods=['POST'])
def upload_image_algo2():
    file_names = []
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('file')
    if len(files) != 1:
        flash("You are only allowed to upload 1 file")
        return render_template("algo2.html")
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template("algo2.html", filenames=file_names)


@app.route('/algo3', methods=['POST'])
def upload_image_algo3():
    return upload_image("algo3.html")


@app.route('/algo4', methods=['POST'])
def upload_image_algo4():
    return upload_image("algo4.html")


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run()
