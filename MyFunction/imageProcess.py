from MyFunction.config import *
import cv2
import yaml_handle
from MyFunction import lib

lab_data = None
def detect_color_item(img, target_color) -> True:
    """if detect color max than DETACT_LIMIT the true
    """
    lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)
    
    frame_resize = cv2.resize(img, (320, 240), interpolation=cv2.INTER_NEAREST)
    img_center_x = frame_resize.shape[:2][1]/2  # 获取缩小图像的宽度值的一半
    img_center_y = frame_resize.shape[:2][0]/2

    frame_lab = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2LAB)  # 将图像转换到 LAB 空间
    frame_mask = cv2.inRange(frame_lab,
                            (lab_data[target_color]['min'][0],
                            lab_data[target_color]['min'][1],
                            lab_data[target_color]['min'][2]),
                            (lab_data[target_color]['max'][0],
                            lab_data[target_color]['max'][1],
                            lab_data[target_color]['max'][2]))  #对原图像和掩模进行位运算    

    opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8))  # 开运算
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE,np.ones((6, 6), np.uint8))  # 闭运算
    contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 找出所有外轮廓

    areaMaxContour, maxvalue = lib.getAreaMaxContour(contours)  # 找到最大的轮廓

    print(maxvalue)

