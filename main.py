import sys,os,json,requests,time
from PyQt5 import QtCore, QtWidgets
import MainSpider,UI

images_num = 0
images_folder_images_num=0

class MyThread(QtCore.QThread):

    sig = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)
        self.Spider = MainSpider.Spider()  # 声明爬虫对象

    def run(self):
        global images_num
        n = 0
        while True:
            self.sig.emit(n)
            if images_folder_images_num > 20:#如果积攒了太多没看的图片Spixiv就会休息一会儿再爬 :)
                time.sleep(images_folder_images_num//2)#休息的时间受积攒的图片数影响
            self.Spider.craw_one()
            images_num += 1
            #n += 1


class Main(QtCore.QObject):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.init_file()
        self.main_ui = UI.MainUI()  # 开启界面
        self._thread = MyThread()
        self._thread.sig.connect(self.catch_buttom)
        self._thread.start()
        
        self.main_ui.show_img_init()
    def init_file(self):
        path = "data/images"
        current_path=os.getcwd()
        if not os.path.exists(path):
            os.makedirs(os.path.join(current_path, path))

    def catch_buttom(self, n):
        global images_num,images_folder_images_num
        if images_num == 0:
            self.main_ui.send_state_msg("(*/ω＼*)感谢使用~正在测试网络...")
        elif images_num == 1:
            self.main_ui.send_state_msg("(๑•̀ㅂ•́)و✧网络正常~开始加载~~~")
        else:
            images_folder_images_num=images_num-self.main_ui.img_cnt #加载过的减去浏览(删除)过的得到剩余未展示的
            self.main_ui.send_state_msg("已加载 {} 张".format(images_num))
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(UI.StyleSheet)
    main = Main()
    app.exec_()
