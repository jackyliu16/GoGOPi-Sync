import cv2

from MyFunction import run
if __name__ == "__main__":
    CAM = cv2.VideoCapture(0)
    resolution = (int(CAM.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(CAM.get(cv2.CAP_PROP_FRAME_WIDTH)))
    run.init(resolution)
    try:
        while True:
            ret, img = CAM.read()
            img = run.run(img)
            cv2.imshow('frame', img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        run.reset()

    CAM.release()
    cv2.destroyAllWindows()
