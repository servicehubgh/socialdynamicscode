import os

from utils.folder_file_manager import make_directory_if_not_exists

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(CUR_DIR, 'utils', 'model')
INPUT_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'input'))
VIDEO_INPUT_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'video_input'))
UPLOAD_FOLDER = make_directory_if_not_exists(os.path.join(CUR_DIR, 'static', 'uploads'))

CAFFEMODEL_PATH = os.path.join(MODEL_DIR, 'SSD_MobileNet.caffemodel')
PROTOTXT_PATH = os.path.join(MODEL_DIR, 'SSD_MobileNet_prototxt.txt')
YOLO_WEIGHT_PATH = os.path.join(MODEL_DIR, 'yolov3.weights')
YOLO_CONFIG_PATH = os.path.join(MODEL_DIR, 'yolov3.cfg')
YOLO_COCO_PATH = os.path.join(MODEL_DIR, 'coco.names')
PB_MODEL_PATH = os.path.join(MODEL_DIR, 'frcnn_inception_v2.pb')
PB_TEXT_PATH = os.path.join(MODEL_DIR, 'frcnn_inception_v2_graph.pbtxt')

DETECT_CONFIDENCE = 0.3
OVERLAP_THRESH = 0.5
SAFE_DISTANCE = 200
FOCUS_LENGTH = 615

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

GPU = True
LOCAL = True
WEB_SERVER = True
