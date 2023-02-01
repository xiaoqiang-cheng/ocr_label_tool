from model import Model
from view import View
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer, Qt, QEventLoop, QCoreApplication

import PySide2
import qdarkstyle
from qdarkstyle.light.palette import LightPalette
from utils import *

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class Controller(object):
    '''
        MVC模式中的 控制器部分 仅用于人机交互的操作与总体调度
    '''
    def __init__(self):
        self.app = QApplication([])
        self.view = View()
        # apply_stylesheet(self.view.ui, "dark_blue.xml")
        self.model = Model()
        self.view.set_slider_image_play_range(0, 0)
        self.image_play_timer = QTimer()
        self.image_play_timer.timeout.connect(self.image_play)
        self.signal_connect()
        self.app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside2", palette = LightPalette))
        self.key_func_map = {
            Qt.Key_Space: self.exec_clear_confirm,
            Qt.Key_Left : self.play_last_frame,
            Qt.Key_Up   : self.exec_image_up,
            Qt.Key_Right: self.play_next_frame,
            Qt.Key_Down : self.exec_image_down,
            Qt.Key_Backspace : self.exec_remove_tail_char
        }
        self.curr_frame_label_char = ""
        self.curr_frame_clear_flag = 1
        self.ground_truth = {}
        self.ground_truth_json_name = ""
        self.image_size = 5.0

        # for update log info
        self.Timer = QTimer()
        self.Timer.start(100)
        self.Timer.timeout.connect(self.monitor_timer)



    def signal_connect(self):
        self.view.ui.button_choose_image.clicked.connect(self.choose_image)
        self.view.ui.checkbox_auto_review.stateChanged.connect(self.image_auto_play)
        self.view.ui.slider_image_play.valueChanged.connect(self.image_slider_change)
        self.view.ui.button_last_frame.clicked.connect(self.play_last_frame)
        self.view.ui.button_next_frame.clicked.connect(self.play_next_frame)
        self.view.text_label_ground_truth.key_connect(self.label_key_event)
        self.view.ui.checkbox_image_clearness.stateChanged.connect(self.clearness_change)
        # self.label_key_event self.view.ui.text_label_ground_truth.keyPressEvent

    def label_key_event(self, ev : PySide2.QtGui.QKeyEvent):
        key = ev.key()

        if key in self.key_func_map.keys():
            self.key_func_map[key]()
        else:
            char = ev.text()
            if char.isdigit() or char.isalpha():
                self.curr_frame_label_char += char

        self.view.set_text_label_ground_truth(self.curr_frame_label_char)
        self.update_ground_truth()

    def clearness_change(self):
        self.curr_frame_clear_flag = self.view.get_state_checkbox_image_clearness()

    def exec_remove_tail_char(self):
        if self.curr_frame_label_char != "":
            self.curr_frame_label_char = self.curr_frame_label_char[:-1]

    def play_next_frame(self):
        self.model.curr_image_index += 1
        if self.model.curr_image_index >= self.model.image_cnt:
            self.model.curr_image_index = 0
        self.update_special_frame_state(self.model.curr_image_index)

    def play_last_frame(self):
        self.model.curr_image_index -= 1
        if self.model.curr_image_index <= 0:
            self.model.curr_image_index = 0
        self.update_special_frame_state(self.model.curr_image_index)

    def exec_clear_confirm(self):
        self.view.set_state_checkbox_image_clearness(not self.curr_frame_clear_flag)

    def exec_image_up(self):
        self.image_size += 0.5
        self.update_img_ui_state()

    def exec_image_down(self):
        self.image_size -= 0.5
        if self.image_size < 1:
            self.image_size = 1
        self.update_img_ui_state()

    def update_ground_truth(self):
        key = self.model.image_list[self.model.curr_image_index]
        self.curr_frame_clear_flag = self.view.get_state_checkbox_image_clearness()
        self.ground_truth[key] = [self.curr_frame_label_char, self.curr_frame_clear_flag]

    def get_curr_ground_truth(self, value):
        key = self.model.image_list[value]
        return self.ground_truth[key]

    def image_slider_change(self, value):
        self.curr_frame_label_char, self.curr_frame_clear_flag = self.get_curr_ground_truth(value)
        self.update_special_frame_state(value)


    def save_ground_truth(self):
        if (self.model.file_image_state):
            write_json(self.ground_truth, self.ground_truth_json_name)

    def image_auto_play(self):
        flag = self.view.get_state_image_auto_play()
        if flag:
            dtime = self.view.get_value_image_dtime()
            self.image_play_timer.start(dtime)
        else:
            self.image_play_timer.stop()

    def image_play(self):
        # if self.model.platvar.image_path == None:
        #     return
        self.model.curr_image_index += 1
        if self.model.curr_image_index >= self.model.image_cnt:
            self.model.curr_image_index = 0

        self.update_special_frame_state(self.model.curr_image_index)

    def update_special_frame_state(self, frame):
        self.model.curr_image_index = frame
        self.update_img_ui_state()

    def update_img_ui_state(self):
        if (self.model.file_image_state):
            self.curr_image_path, unix_time, bj_time, img = \
                        self.model.get_curr_frame_image_info()

            self.view.update_cv_image(self.curr_image_path, self.image_size)
            self.view.update_label_unix_time(unix_time)
            self.view.update_label_beijing_time(bj_time)
            self.view.update_text_curr_image_frame(self.model.curr_image_index, self.model.image_cnt-1)
            self.view.set_slider_image_play_value(self.model.curr_image_index)
            self.view.set_image_ratio_value(self.image_size)
            self.view.set_text_label_ground_truth(self.curr_frame_label_char)
            self.view.set_state_checkbox_image_clearness(self.curr_frame_clear_flag)

    def choose_image(self):
        image_path = choose_folder(self.view.ui, "选择image文件夹", self.model.image_path)
        if not image_path :
            return

        # image_path = "/home/uisee/MainDisk/Develop/cv_uos/install/data/light_number_patch"
        self.model.check_image_path(image_path)
        filename = os.path.split(image_path)[1]
        self.ground_truth_json_name = os.path.join(image_path, filename + ".json")

        if os.path.exists(self.ground_truth_json_name):
            self.ground_truth = fast_parse_json(self.ground_truth_json_name)
        else:
            self.ground_truth = {}
            for x in self.model.image_list:
                self.ground_truth[x] = ["", 1]

        self.view.update_image_path(image_path)
        self.view.set_slider_image_play_range(0, self.model.image_cnt - 1)
        self.view.set_slider_image_play_value(0)
        self.update_special_frame_state(0)

    def run(self):
        self.view.show()
        self.app.exec_()
        self.Timer.stop()
        self.save_ground_truth()

    def sigint_handler(self, signum = None, frame = None):
        import sys
        self.Timer.stop()
        sys.exit(self.app.exec_())


    def monitor_timer(self):
        self.save_ground_truth()





if __name__ == "__main__":
    obj = Controller()
    obj.run()

