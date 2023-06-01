from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory, Response
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash
from werkzeug.utils import secure_filename
import pipeline

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
# ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF'}

config = {
    "DEBUG": True
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.secret_key = 'key'

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/assessment', methods=['GET', 'POST'])
def upload_and_classify():
    if request.method == 'POST':

        file = request.files['file']

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        model_results = pipeline.pipe(filepath)
        print(type(model_results))
        return render_template('results.html', result=model_results, scroll='third', filename=filename)

    flash('Invalid file format. Please try again.')
    return redirect(url_for('assess'))


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host='0.0.0.0')