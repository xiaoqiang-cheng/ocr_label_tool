import os
from utils import *
import time

class Model:
    def __init__(self):
        self.image_path = "."
        self.image_path_dict = {}
        self.img_image_list = []
        self.img_ext_name = "jpg"
        self.image_list = []
        self.image_cnt = 0
        self.file_image_state = False
        self.curr_image_index = 0

    def check_image_path(self, image_path):
        if not os.path.exists(image_path):
            return False

        self.image_path_dict = {}
        list_find_files(image_path, (".png", ".jpg", ".tiff", ".bmp"), self.image_path_dict)
        self.img_image_list = list(self.image_path_dict.keys())
        self.img_image_list.sort()
        self.curr_image_index = 0
        if len(self.img_image_list) != 0:
            self.img_ext_name = os.path.splitext(self.image_path_dict[self.img_image_list[0]])[-1][1:]
        else:
            self.img_ext_name = "jpg"

        self.image_list = self.img_image_list
        self.image_cnt = len(self.image_list)

        self.image_path = image_path
        self.file_image_state = True

        return True


    def get_curr_frame_image_info(self):
        if self.image_list[self.curr_image_index] not in self.image_path_dict.keys():
            img_path = os.path.join(self.image_path,
                            self.image_list[self.curr_image_index] + ".%s"%self.img_ext_name)
        else:
            img_path = self.image_path_dict[self.image_list[self.curr_image_index]]

        unix_time = self.image_list[self.curr_image_index]
        try:
            timeArray = time.localtime(float(unix_time))
            beijing_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            beijing_time = beijing_time + "." + unix_time.split(".")[-1]
        except:
            beijing_time = "can not show time"
        # img = cv2.imread(img_path)
        return img_path, unix_time, beijing_time, img_path
