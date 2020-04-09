import sys,requests,time
from PyQt5 import QtCore, QtWidgets
import UI,MainSpider

images_num=0
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
            self.Spider.craw_one()
            images_num+=1
            # time.sleep(0.3)
            n += 1

class Main(QtCore.QObject):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self._thread = MyThread()
        self._thread.sig.connect(self.catch_buttom)
        self._thread.start()
        self.main_ui = UI.MainUI()  # 开启界面
        self.main_ui.show_img_init()
    def catch_buttom(self, n):
        global images_num
        self.main_ui.send_state_msg("已加载{}张图片".format(images_num))


app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(UI.StyleSheet)
main = Main()  
app.exec_()



'''
def Start_MainSpider():
    print(1)
    Spider=MainSpider.Spider()
    Spider.craw_base_urls()

class img_manager():
    def __init__(self):
        self.local_img_url_list=[]
    def get_local_img(self):
        if len(self.local_img_url_list) == 0:
            return None
        local_img_url=self.local_img_url_list.pop()
        return local_img_url
    def store_local_img(self,local_img_url):
        if local_img_url is None:
            return
        self.local_img_url_list.append(local_img_url)
    def local_img_num(self):
        return len(self.local_img_url_list)
'''
