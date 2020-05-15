import glob
import os

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
from src.social_distance.estimator import SocialDistanceEstimator
from settings import WEB_SERVER, UPLOAD_FOLDER, SERVER_HOST, SERVER_PORT, INPUT_DIR

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


@app.route('/upload', methods=['POST'])
def success():
    if request.method == 'POST':
        for tmp_path in glob.glob(os.path.join(INPUT_DIR, "*.*")):
            os.remove(tmp_path)

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        file_path = os.path.join(INPUT_DIR, secure_filename(file.filename))
        file.save(file_path)

        filename, result_info = social_estimator.process_one_frame(frame_path=file_path)

        flash('Image successfully uploaded and Estimated')
        return render_template('file_upload_form.html', filename=filename, data=result_info)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    social_estimator = SocialDistanceEstimator()

    if WEB_SERVER:
        app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
    else:
        social_estimator.process_one_frame(frame_path="")
