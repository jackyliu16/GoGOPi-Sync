import cv2
import numpy as np

__BinarizationThreshold = 80


def binary_image(frame):
    global resolution
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, __BinarizationThreshold, 255, cv2.THRESH_BINARY)

    __mask = np.zeros(resolution, dtype=np.uint8)
    # rectangle_mask = (__mask, resolution)
    # __mask = cv2.rectangle(__mask, (int(resolution[0] * 0.75), 0), (int(resolution[0] * 0.80), resolution[1]), (255))
    __mask = cv2.rectangle(__mask, (0, int(resolution[0]*0.75)), (resolution[1], int(resolution[0]*0.8)), 255, thickness=-1)

    mask = cv2.bitwise_not(__mask, None)
    masked_img = cv2.bitwise_and(binary, binary, mask=__mask)

    return masked_img

if __name__ == "__main__":
    global resolution
    cap = cv2.VideoCapture(0)
    
    resolution = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(resolution)
    while True:
        ret, frame = cap.read()
        binary = binary_image(frame)
        cv2.imshow('frame', binary)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
