import cv2
import numpy

from init import *

cap = cv2.VideoCapture(0)

def GetImage_thrfunc():
    global frame
    while True:
        frame = cap.read()[1]

get_image_thr = threading.Thread(target = GetImage_thrfunc)
get_image_thr.start()

config = 0

def CalcConfig():
    global config
    if frame is None:
        return 0
    diff_row = numpy.mean(numpy.abs(frame[64] - [100, 180, 240]), axis = -1).astype(numpy.uint8)
    bool_row = diff_row < 48

    width = frame.shape[1]
    neighbor = 2
    bool_row = [(lambda li: any(li) and all(li))(bool_row[
        index  - neighbor : index + neighbor + 1
    ]) for index in range(width)]
    if any(bool_row):
        center = numpy.mean(numpy.extract(bool_row, numpy.arange(width))).__int__()
        config = center - width // 2
        return config
    print("No capture")
    return config

if __name__ == "__main__":
    while True:
        print(CalcConfig())
        if frame is None:
            continue
        cv2.imshow("image", frame)
        cv2.waitKey(1)