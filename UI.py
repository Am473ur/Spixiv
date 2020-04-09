import sys
from PyQt5 import QtWidgets,QtGui,QtCore
import ImgDownloader
StyleSheet = '''
QWidget#main_widget{
    border-radius:30px;
}

QTextEdit{
    font-family: "Microsoft YaHei";
}

QPushButton {
    border: none; /*去掉边框*/
}

#right_close {
    background: #F76677;
    border-radius: 15px; /*圆角*/
}
#right_close:hover {
    background-color: red;
}
#right_close:pressed {
    background-color: #a41320;
}

#next_img {
    background-color: #85cbeb;
    border-radius: 5px; /*圆角*/
}
#next_img:hover {
    background-color: #9fd3eb;
}
#next_img:pressed {
    background-color: #c3e1ef;
}

#save_img {
    background-color: #eaaf6f;
    border-radius: 5px; /*圆角*/
}
#save_img:hover {
    background-color: #eabc8a;
}
#save_img:pressed {
    background-color: #eacaa7;
}

#about{
    font-size:24px;
    color: #eacaa7;
}
#stateView{
    font-family: "Microsoft YaHei";
    color: #b555f8;
}

'''

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI() #界面绘制交给InitUi方法
    def initUI(self):
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_widget.setObjectName('main_widget')
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.setCentralWidget(self.main_widget)
        self.position_table()
        self.main_layout.setSpacing(0)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)   #将Form设置为透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint) #将Form设置为无边框
        desktop = QtWidgets.QApplication.desktop()
        #print(desktop.width(),desktop.height())
        self.setFixedSize(desktop.width(),desktop.height()-40)
        self.showMaximized()#打开时默认窗口为最大化显示
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap("backguarnd_imgs/backguarnd_img.png")#背景图片
        painter.drawPixmap(self.rect(), pixmap)

    def position_table(self):
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格
 
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget,0,0,9,85) # 左侧部件在第0行第0列，占10行9列
        self.main_layout.addWidget(self.right_widget,0,85,9,15) # 右侧部件在第0行第9列，占10行1列

        self.stateView = QtWidgets.QPlainTextEdit(self,objectName="stateView")#文本框
        self.stateView.setReadOnly(True)#文本框只读

        self.right_close = QtWidgets.QPushButton("×", self,objectName="right_close") # 关闭按钮
        self.right_close.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.right_close.setFixedSize(36,36) # 设置关闭按钮的大小

        self.next_img = QtWidgets.QPushButton(" ", self,objectName="next_img")
        self.next_img.setFixedSize(240,200)
        self.next_img.clicked.connect(self.click_next_img)
        self.save_img = QtWidgets.QPushButton(" ", self,objectName="save_img")
        self.save_img.setFixedSize(240,60)
        self.save_img.clicked.connect(self.click_save_img)

        self.zhanwei = QtWidgets.QPushButton(" ", self,objectName="zhanwei")
        self.zhanwei.setFixedSize(240,200)

        self.about = QtWidgets.QPushButton("CaoYi", self,objectName="about")
        self.about.setFixedSize(80,50)
        #self.about.clicked.connect(self.about)

        #self.right_layout.addWidget(self.right_mini,0,94,1,2,QtCore.Qt.AlignTop)
        self.right_layout.addWidget(self.right_close,0,97,1,2,QtCore.Qt.AlignTop)#关闭
        self.right_layout.addWidget(self.stateView,1,85,3,15,QtCore.Qt.AlignTop)#只读文本框（状态）
        self.right_layout.addWidget(self.next_img,4,85,2,15,QtCore.Qt.AlignCenter)#下一张
        self.right_layout.addWidget(self.save_img,6,85,2,15,QtCore.Qt.AlignCenter)#保存
        self.right_layout.addWidget(self.zhanwei,8,85,1,15)#占位
        self.right_layout.addWidget(self.about,8,85,1,15,QtCore.Qt.AlignCenter)#关于

    def show_img_init(self):
        self.img_cnt=0
        self.img_box = QtWidgets.QWidget()
        self.painter = QtWidgets.QLabel(self.img_box)
        self.painter.setObjectName('painter')
        #self.painter.setGeometry(QtCore.QRect(1, 1, 800, 600))
        self.img_manager=ImgDownloader.img_manager()
    def click_next_img(self):
        
        local_img_url=str(self.img_manager.get_local_img())
        if local_img_url=="None":
            self.send_state_msg("点的太快啦~")
            return None
        else:
            self.img_cnt+=1
            self.send_state_msg(local_img_url)
            self.stateView.appendPlainText('现在是第{}张'.format(self.img_cnt))
        local_img_url="data\\img_mini\\"+local_img_url
        pixmap = QtGui.QPixmap(local_img_url)
        self.painter.setPixmap(pixmap)
        
        self.painter.setScaledContents(True)
        self.left_layout.addWidget(self.painter,0,0,9,85,QtCore.Qt.AlignCenter)
    def click_save_img(self):
        self.stateView.appendPlainText('啦啦啦啦~')

    def send_state_msg(self,msg):
        self.stateView.appendPlainText(msg)

def Start_UI():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    ex = MainUI()
    sys.exit(app.exec_()) 
#Start_UI()