import sys,base64,os,json,shutil,time
from PyQt5 import QtWidgets,QtGui,QtCore
import ImgDownloader
from img_b64 import img_b64
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
    font-family: "Microsoft YaHei";
    color: white;
    font-size:30px;
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
    font-family: "Microsoft YaHei";
    font-size:30px;
    color: white;
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
    font-family: "Microsoft YaHei";
    font-size:24px;
    color: #eacaa7;
}
#stateView{
    font-family: "Microsoft YaHei";
    color: #b555f8;
}
#delet_img {
    font-family: "Microsoft YaHei";
    color: white;
    font-size:24px;
    background-color: #cf4858;
    border-radius: 5px; /*圆角*/
}
#delet_img:hover {
    background-color: #cd6470;
}
#delet_img:pressed {
    background-color: #cb858d;
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
        img_data = base64.b64decode(img_b64)
        with open('data\\backguarnd.png', 'wb') as f:
            f.write(img_data)
        pixmap = QtGui.QPixmap("data\\backguarnd.png")#背景图片
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

        self.main_layout.addWidget(self.left_widget,0,0,9,85) # 左侧部件在第0行第0列，占9行85列
        self.main_layout.addWidget(self.right_widget,0,85,9,15) # 右侧部件在第0行第85列，占9行15列

        self.stateView = QtWidgets.QPlainTextEdit(self,objectName="stateView")#文本框
        self.stateView.setReadOnly(True)#文本框只读

        self.right_close = QtWidgets.QPushButton("×", self,objectName="right_close") # 关闭按钮
        self.right_close.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.right_close.setFixedSize(36,36) # 设置关闭按钮的大小

        self.next_img = QtWidgets.QPushButton("Next", self,objectName="next_img") #next_img按钮
        self.next_img.setFixedSize(240,200)
        self.next_img.clicked.connect(self.click_next_img)
        self.save_img = QtWidgets.QPushButton("Save", self,objectName="save_img") #save_img按钮
        self.save_img.setFixedSize(240,60)
        self.save_img.clicked.connect(self.click_save_img)
        #self.right_close = QtWidgets.QPushButton("清除缓存并退出", self,objectName="delet_img") #delet_img按钮
        #self.save_img.setFixedSize(240,30)
        #self.save_img.clicked.connect(self.click_save_img)

        self.delet_img = QtWidgets.QPushButton("清除缓存并退出", self,objectName="delet_img")
        self.delet_img.setFixedSize(240,60)
        self.delet_img.clicked.connect(self.click_delet_img)#先触发事件 清除缓存
        self.delet_img.clicked.connect(QtCore.QCoreApplication.instance().quit)#再退出

        self.about = QtWidgets.QPushButton("CaoYi", self,objectName="about")
        self.about.setFixedSize(240,60)
        #self.about.clicked.connect(self.about)

        #self.right_layout.addWidget(self.right_mini,0,94,1,2,QtCore.Qt.AlignTop)
        self.right_layout.addWidget(self.right_close,0,97,1,2,QtCore.Qt.AlignTop)#关闭
        self.right_layout.addWidget(self.stateView,1,85,3,15,QtCore.Qt.AlignTop)#只读文本框（状态）
        self.right_layout.addWidget(self.next_img,4,85,2,15,QtCore.Qt.AlignCenter)#下一张
        self.right_layout.addWidget(self.save_img,6,85,1,15,QtCore.Qt.AlignCenter)#保存
        self.right_layout.addWidget(self.delet_img,7,85,1,15,QtCore.Qt.AlignCenter)#delete_img
        self.right_layout.addWidget(self.about,8,85,1,15,QtCore.Qt.AlignCenter)#关于
        #self.right_layout.addWidget(self.save_img,9,85,1,15,QtCore.Qt.AlignCenter)#delete_img

    def show_img_init(self):
        self.img_cnt=0
        self.img_box = QtWidgets.QWidget()
        self.painter = QtWidgets.QLabel(self.img_box)
        self.painter.setObjectName('painter')
        #self.painter.setGeometry(QtCore.QRect(1, 1, 800, 600))
        self.img_manager=ImgDownloader.img_manager()
        self.local_img_url="None"
    def click_delet_img(self):
        shutil.rmtree("data\\images")
        
    def click_next_img(self):
        if os.path.exists(self.local_img_url):
            os.remove(self.local_img_url)#删除临时文件夹中的图片
            #self.stateView.appendPlainText('删除成功')
        else:
            pass
            #self.stateView.appendPlainText('删除{}失败'.format(self.local_img_url))

        self.local_img_url=str(self.img_manager.get_local_img())# pop 出一个图片名
        if self.local_img_url=="None":
            self.send_state_msg("(＞﹏＜)点得太快啦~")
            return None
        else:
            self.img_cnt+=1
            self.send_state_msg(self.local_img_url)
            self.stateView.appendPlainText('这是第 {} 张'.format(self.img_cnt))
        
        self.local_img_url="data\\images\\"+self.local_img_url # 把图片名拼成地址
        pixmap = QtGui.QPixmap(self.local_img_url)
        self.painter.setPixmap(pixmap)
        self.painter.setScaledContents(True)
        self.left_layout.addWidget(self.painter,0,0,9,85,QtCore.Qt.AlignCenter)
    def click_save_img(self):
        #self.stateView.appendPlainText('当前图片是{}'.format(self.local_img_url))
        img_save_path=self.get_img_save_path() #从 Setting.json 中获取图片保存路径
        if not os.path.exists(img_save_path): #如果文件夹不存在，就创建一个
            self.stateView.appendPlainText('创建 ' + img_save_path + ' 文件夹')
            os.makedirs(img_save_path)
        if self.local_img_url=="None":
            self.stateView.appendPlainText('(/= _ =)/~┴┴ 找不到图片啊~')
        else:
            shutil.copy(self.local_img_url, img_save_path)
            self.stateView.appendPlainText('嘿嘿嘿~保存成功！')
    def get_img_save_path(self):
        f = open("Settings.json", encoding='utf-8')
        setting = json.load(f)
        img_save_path=setting[0]["img_save_path"]
        return img_save_path

    def send_state_msg(self,msg):
        self.stateView.appendPlainText(msg)
'''
def Start_UI():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    ex = MainUI()
    sys.exit(app.exec_()) 
#Start_UI()
'''