import glob
import os

from flask import Flask, render_template, request, url_for, flash, redirect
from flask_cors import CORS
from werkzeug.utils import secure_filename
from src.social_distance.estimator import SocialDistanceEstimator
from settings import WEB_SERVER, UPLOAD_FOLDER, SERVER_HOST, SERVER_PORT, INPUT_DIR
from utils.folder_file_manager import log_print


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
social_estimator = SocialDistanceEstimator()


@app.route('/')
def upload():
    return render_template("main.html")


@app.route('/video_upload')
def upload_video():
    return render_template("detail.html")


@app.route('/image_upload')
def upload_image():
    return render_template("file_upload_form.html")


@app.route('/upload', methods=['POST'])
def success():
    try:
        if request.method == 'POST':
            for tmp_path in glob.glob(os.path.join(INPUT_DIR, "*.*")):
                os.remove(tmp_path)
            for tmp_path in glob.glob(os.path.join(UPLOAD_FOLDER, "*.*")):
                os.remove(tmp_path)

            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                message = 'Click on Choose File button to select picture before uploading'
                return render_template('file_upload_form.html', messages=message, filename=None, data=None)
            file_path = os.path.join(INPUT_DIR, secure_filename(file.filename))
            file.save(file_path)

            filename, result_info = social_estimator.process_one_frame(frame_path=file_path)

            message = 'Image successfully uploaded and Estimated'
            return render_template('file_upload_form.html', messages=message, filename=filename, data=result_info)
    except Exception as e:
        log_print(info_str=e)
        return render_template('file_upload_form.html', messages=e, filename=None, data=None)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/video', methods=['POST'])
def display_video_stream():
    frame = request.files['image']
    frame_path = os.path.join(INPUT_DIR, "video.jpg")
    frame.save(frame_path)
    filename, result_info = social_estimator.process_one_frame(frame_path=frame_path)
    send_frame = open(os.path.join(UPLOAD_FOLDER, filename), 'rb').read()
    # response = {'image': "send_frame"}

    return send_frame


if __name__ == '__main__':

    if WEB_SERVER:
        app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
    else:
        social_estimator.process_one_frame(frame_path="")
