import os
import time
import cv2
import numpy as np
import ntpath

from src.person.detector import PersonDetector
from src.social_distance.calculator import calculate_real_distance_two_persons
from src.person.nms import non_max_suppression_slow
from utils.folder_file_manager import log_print
from settings import SAFE_DISTANCE, UPLOAD_FOLDER


class SocialDistanceEstimator:

    def __init__(self):
        self.person_detector = PersonDetector()

    def main(self, vid_path=None):

        if vid_path is None:
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(vid_path)

        while True:

            ret, frame = cap.read()
            if not ret:
                break
            result_frame = self.process_one_frame(frame_path=frame)

            cv2.imshow('Social Distancing Analyser', result_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    def process_one_frame(self, frame_path):

        social_distance_result = {
            "danger": [],
            "safe": []
        }

        frame = cv2.imread(frame_path)
        height, width = frame.shape[:2]
        file_name = ntpath.basename(frame_path)

        st_time = time.time()
        boxes, confidences = self.person_detector.detect_person_yolo(frame=frame)
        filtered_idx, _ = non_max_suppression_slow(boxes=np.array(boxes), keys=range(len(boxes)))
        # filtered_idx = cv2.dnn.NMSBoxes(boxes, confidences, DETECT_CONFIDENCE, OVERLAP_THRESH)
        print(time.time() - st_time)
        if len(filtered_idx) > 0:
            # idf = filtered_idx.flatten()
            center = []
            distance = {}
            for i in filtered_idx:
                (x1, y1) = (boxes[i][0], boxes[i][1])
                (x2, y2) = (boxes[i][2], boxes[i][3])
                center.append([x1, y1, x2, y2])
            for i in range(len(center)):
                distance["person_{}".format(i)] = {}
                for j in range(len(center)):
                    if i == j:
                        continue
                    try:
                        geometry = calculate_real_distance_two_persons(center[i], center[j])
                    except Exception as e:
                        log_print(info_str=e)
                        geometry = 0
                    distance["person_{}".format(i)][j] = geometry

            for i in range(len(center)):
                left, top, right, bottom = center[i]
                text = "person_" + str(i + 1)
                inter_dist = []
                inter_person_id = []
                close_ret = False
                for j in distance["person_{}".format(i)].keys():
                    if i == j:
                        continue
                    if distance["person_{}".format(i)][j] <= SAFE_DISTANCE:
                        inter_dist.append(distance["person_{}".format(i)][j])
                        inter_person_id.append(j)
                        close_ret = True
                if close_ret:
                    min_dist = min(inter_dist)
                    min_person_id = inter_person_id[inter_dist.index(min_dist)]
                    warning_str = text + "; " + "person_" + str(min_person_id + 1) + ":" + str(min_dist) + "cm"
                    social_distance_result["danger"].append(warning_str)
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    # cv2.putText(frame, warning_str, (x, max(y - 10, 0)), cv2.FONT_HERSHEY_TRIPLEX, 1,
                    #             (0, 0, 255), 2)
                else:
                    social_distance_result["safe"].append(text)
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, str(i + 1), (left, max(top - 3, 0)), cv2.FONT_HERSHEY_TRIPLEX, height / 1500,
                            (0, 255, 0), 3)

        print(social_distance_result)
        if width >= 800:
            fx = 800 / width
        else:
            fx = 1

        cv2.imwrite(os.path.join(UPLOAD_FOLDER, file_name), cv2.resize(frame, None, fx=fx, fy=fx))
        # cv2.imshow("social distance", frame)
        # cv2.waitKey()

        return file_name, social_distance_result


if __name__ == '__main__':

    SocialDistanceEstimator().process_one_frame(frame_path="")
