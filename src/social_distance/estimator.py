import time
import cv2

from src.person.detector import PersonDetector
from src.social_distance.calculator import calculate_real_distance_two_persons
from utils.folder_file_manager import log_print
from settings import DETECT_CONFIDENCE, DETECT_THRESH, SAFE_DISTANCE


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
            result_frame = self.process_one_frame(frame=frame)

            cv2.imshow('Social Distancing Analyser', result_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    def process_one_frame(self, frame):

        st_time = time.time()
        boxes, confidences = self.person_detector.detect_person_tensorflow(frame=frame)

        idx = cv2.dnn.NMSBoxes(boxes, confidences, DETECT_CONFIDENCE, DETECT_THRESH)
        print(time.time() - st_time)
        if len(idx) > 0:
            idf = idx.flatten()
            center = list()
            distance = {}
            for i in idf:
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                center.append([x, y, x + w, y + h])
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

            for i in idf:
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                text = "person_" + str(i)
                inter_dist = []
                inter_person_id = []
                close_ret = False
                dist_index = list(idf).index(i)
                for j in distance["person_{}".format(dist_index)].keys():
                    if distance["person_{}".format(dist_index)][j] <= SAFE_DISTANCE:
                        inter_dist.append(distance["person_{}".format(dist_index)][j])
                        inter_person_id.append(j)
                        close_ret = True
                if close_ret:
                    min_dist = min(inter_dist)
                    min_person_id = inter_person_id[inter_dist.index(min_dist)]
                    warning_str = text + ";" + "person_" + str(min_person_id) + ":" + str(min_dist) + "cm"
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, warning_str, (x, max(y - 10, 0)), cv2.FONT_HERSHEY_TRIPLEX, 1,
                                (0, 0, 255), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, text, (x, max(y - 10, 0)), cv2.FONT_HERSHEY_TRIPLEX, 1,
                                (0, 255, 0), 2)

        return frame


if __name__ == '__main__':

    SocialDistanceEstimator().main(vid_path="/media/mensa/Data/Task/SocialDistance/video.mp4")
