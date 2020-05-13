import numpy as np

from settings import OVERLAP_THRESH


def non_max_suppression_slow(boxes, keys):

    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []
    # initialize the list of picked indexes
    pick = []
    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # compute the area of the bounding boxes and sort the bounding boxes by the bottom-right y-coordinate
    # of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    id_xs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes list
    while len(id_xs) > 0:

        # grab the last index in the indexes list, add the index value to the list of picked indexes, then initialize
        # the suppression list (i.e. indexes that will be deleted) using the last index
        last = len(id_xs) - 1
        i = id_xs[last]
        pick.append(i)
        suppress = [last]

        # loop over all indexes in the indexes list
        for pos in range(0, last):

            # grab the current index
            j = id_xs[pos]

            # find the largest (x, y) coordinates for the start of the bounding box and the smallest (x, y) coordinates
            # for the end of the bounding box
            xx1 = max(x1[i], x1[j])
            yy1 = max(y1[i], y1[j])
            xx2 = min(x2[i], x2[j])
            yy2 = min(y2[i], y2[j])

            # compute the width and height of the bounding box
            w = max(0, xx2 - xx1 + 1)
            h = max(0, yy2 - yy1 + 1)
            # compute the ratio of overlap between the computed bounding box and the bounding box in the area list
            overlap = float(w * h) / area[j]

            # if there is sufficient overlap, suppress the current bounding box
            if overlap > OVERLAP_THRESH:
                suppress.append(pos)
        # delete all indexes from the index list that are in the
        # suppression list
        id_xs = np.delete(id_xs, suppress)

    non_picks = []
    for i in range(len(boxes)):
        if i not in pick:
            non_picks.append(keys[i])

    # return only the bounding boxes that were picked
    return pick, non_picks


if __name__ == '__main__':
    non_max_suppression_slow(boxes=np.array([
        [12, 84, 140, 212],
        [114, 60, 178, 124],
        [24, 84, 152, 212],
        [36, 84, 164, 212],
        [12, 30, 76, 94],
        [120, 60, 184, 124],
    ]), keys=[1, 2, 4, 7, 8, 10])
