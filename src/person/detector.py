import cv2
import numpy as np

from settings import CAFFEMODEL_PATH, PROTOTXT_PATH, DETECT_CONFIDENCE, YOLO_COCO_PATH, YOLO_CONFIG_PATH, \
    YOLO_WEIGHT_PATH, GPU, PB_MODEL_PATH, PB_TEXT_PATH


class PersonDetector:

    def __init__(self):
        self.caffe_net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, CAFFEMODEL_PATH)
        # self.yolo_net = cv2.dnn.readNetFromDarknet(YOLO_CONFIG_PATH, YOLO_WEIGHT_PATH)
        # self.coco_labels = open(YOLO_COCO_PATH).read().strip().split("\n")
        # self.ln = self.yolo_net.getLayerNames()
        # self.ln = [self.ln[i[0] - 1] for i in self.yolo_net.getUnconnectedOutLayers()]
        self.cv_net = cv2.dnn.readNetFromTensorflow(PB_MODEL_PATH, PB_TEXT_PATH)
        if GPU:
            self.caffe_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.caffe_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            self.cv_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.cv_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
            # self.yolo_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            # self.yolo_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def detect_person_caffe(self, frame):

        person_boxes = []
        person_confidences = []
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        self.caffe_net.setInput(blob)
        detections = self.caffe_net.forward()

        for i in range(detections.shape[2]):

            confidence = detections[0, 0, i, 2]
            if confidence > DETECT_CONFIDENCE:

                class_id = int(detections[0, 0, i, 1])
                if class_id == 15.00:

                    box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                    left, top, right, bottom = box
                    person_boxes.append([int(left), int(top), int(right - left), int(bottom - top)])
                    person_confidences.append(float(confidence))

        return person_boxes, person_confidences

    def detect_person_yolo(self, frame):

        person_boxes = []
        person_confidences = []

        resized_frame = cv2.resize(frame, (300, 300))
        w_resized_ratio = frame.shape[1] / 300
        h_resized_ratio = frame.shape[0] / 300
        height, width = resized_frame.shape[:2]

        blob = cv2.dnn.blobFromImage(resized_frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.yolo_net.setInput(blob)

        layer_outputs = self.yolo_net.forward(self.ln)
        for output in layer_outputs:

            for detection in output:

                scores = detection[5:]
                class_id = int(np.argmax(scores))
                confidence = scores[class_id]
                if self.coco_labels[class_id] == "person":
                    if confidence > DETECT_CONFIDENCE:

                        box = detection[0:4] * np.array([width, height, width, height])
                        (center_x, center_y, p_width, p_height) = box.astype("int")

                        x = int((center_x - (p_width / 2)) * w_resized_ratio)
                        y = int((center_y - (p_height / 2)) * h_resized_ratio)
                        person_boxes.append([x, y, int(p_width * w_resized_ratio), int(p_height * h_resized_ratio)])
                        person_confidences.append(float(confidence))

        return person_boxes, person_confidences

    def detect_person_tensorflow(self, frame):

        height, width = frame.shape[:2]
        self.cv_net.setInput(cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False))
        cv_out = self.cv_net.forward()

        person_boxes = []
        confidences = []
        for detection in cv_out[0, 0, :, :]:
            score = float(detection[2])
            label = int(detection[1])
            if label == 0:
                if score > DETECT_CONFIDENCE:
                    left = detection[3] * width
                    top = detection[4] * height
                    right = detection[5] * width
                    bottom = detection[6] * height
                    person_boxes.append([int(left), int(top), int(right - left), int(bottom - top)])
                    confidences.append(float(score))

        return person_boxes, confidences


if __name__ == '__main__':
    person_detector = PersonDetector()
    cap = cv2.VideoCapture("")
    while True:
        _, frame_ = cap.read()
        boxes, _ = person_detector.detect_person_yolo(frame=frame_)
        for box_ in boxes:
            cv2.rectangle(frame_, (box_[0], box_[1]), (box_[0] + box_[2], box_[1] + box_[3]), (0, 0, 255), 2)
        cv2.imshow("person", frame_)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
