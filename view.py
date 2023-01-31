from PySide2.QtWidgets import QApplication, QStyleFactory, QCompleter,QLineEdit, QGroupBox, QCheckBox, QVBoxLayout, QLabel, QRadioButton, QHBoxLayout, QWidget, QSplitter, QScrollArea
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QStringListModel,Qt, QSize
from PySide2 import QtGui
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtGui import QTextDocument, QPalette, QTextCursor
import PySide2


class LabelEdit(QLineEdit):
    def key_connect(self, func):
        self.key_callback_fun = func

    def keyPressEvent(self, ev: PySide2.QtGui.QKeyEvent):
        self.key_callback_fun(ev)


class View():
    '''
        mvc模式中的视图部分，本身不包含任何逻辑，仅作界面显示使用
    '''
    def __init__(self):
        self.ui = QUiLoader().load('config/main.ui')
        self.text_label_ground_truth = LabelEdit()
        self.ui.layout_label_text.addWidget(self.text_label_ground_truth)
    def show(self):
        self.ui.show()

    def update_label_image(self, image_path, image_size = (50, 50)):
        pix = QPixmap(image_path)
        pix = pix.scaled(image_size[0], image_size[1], Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.ui.label_image.setPixmap(pix)
        self.ui.label_image.setScaledContents(True)

    def set_text_label_ground_truth(self, char):
        self.text_label_ground_truth.setText(char)


    def cvimg_to_qtimg(self, cvimg):
        height, width,_ = cvimg.shape
        cvimg = QImage(cvimg.data)
        return QPixmap(cvimg)

    def update_cv_image(self, cvimg, image_size_ratio=5.0):
        pix = QPixmap(cvimg)
        pix = pix.scaled(pix.size() * image_size_ratio)
        self.ui.label_image.setPixmap(pix)
        self.ui.label_image.setScaledContents(True)

    def update_label_unix_time(self, value):
        self.ui.label_unix_timestamp.setText(value)

    def update_label_beijing_time(self, value):
        self.ui.label_beijing_timestamp.setText(value)

    def update_image_path(self, path):
        self.ui.text_image_path.setText(path)

    def update_text_curr_image_frame(self, cnt, end_frame):
        self.ui.label_frame_cnt.setText(str(cnt) + " / " + str(end_frame))

    def get_state_image_auto_play(self):
        if (self.ui.checkbox_auto_review.isChecked()):
            return True
        else:
            return False

    def get_state_checkbox_image_clearness(self):
        if (self.ui.checkbox_image_clearness.isChecked()):
            return 1
        else:
            return 0

    def set_state_checkbox_image_clearness(self, state):
        self.ui.checkbox_image_clearness.setChecked(state)

    def set_slider_image_play_range(self, min_value, max_value):
        self.ui.slider_image_play.setMinimum(min_value)
        self.ui.slider_image_play.setMaximum(max_value)

    def set_slider_image_play_value(self, value):
        self.ui.slider_image_play.setValue(value)

    def get_value_image_dtime(self):
        return int(self.ui.text_auto_time.text())

    def set_image_ratio_value(self, ratio):
        self.ui.label_image_ratio.setText(str(ratio))


if __name__ == '__main__':
    import sys
    app = QApplication([])
    obj = View()
    obj.show()
    app.exec_()
