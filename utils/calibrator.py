from settings import SAFE_DISTANCE


def calibrated_dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + 550 / ((p1[1] + p2[1]) / 2) * (p1[1] - p2[1]) ** 2) ** 0.5


def is_close(p1, p2):

    status = 0
    c_d = calibrated_dist(p1, p2)
    calibration = (p1[1] + p2[1]) / 2
    distance = int(SAFE_DISTANCE * c_d / (0.2 * calibration))
    if 0 < c_d < 0.2 * calibration:
        status = 1
        return status, distance
    else:
        return status, distance


if __name__ == '__main__':

    is_close(p1="", p2="")
