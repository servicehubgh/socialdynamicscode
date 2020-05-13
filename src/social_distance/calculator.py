from math import pow, sqrt
from settings import FOCUS_LENGTH


def calculate_real_xyz(rect):
    x_mid = round((rect[0] + rect[2]) / 2, 4)
    y_mid = round((rect[1] + rect[3]) / 2, 4)

    height = round(rect[3] - rect[1], 4)

    # Distance from camera based on triangle similarity
    z_cm = (165 * FOCUS_LENGTH) / height

    # Mid-point of bounding boxes (in cm) based on triangle similarity technique
    x_cm = (x_mid * z_cm) / FOCUS_LENGTH
    y_cm = (y_mid * z_cm) / FOCUS_LENGTH

    return x_cm, y_cm, z_cm


def calculate_real_distance_two_persons(rect_1, rect_2):

    x1, y1, z1 = calculate_real_xyz(rect=rect_1)
    x2, y2, z2 = calculate_real_xyz(rect=rect_2)

    dist = int(sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2)))

    return dist


if __name__ == '__main__':
    calculate_real_distance_two_persons(rect_1=[], rect_2=[])
