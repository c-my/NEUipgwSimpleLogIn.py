from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import requests

# Type your id and password here
username = ""
password = ""


class Login:
    """A class for sign in the ipgw."""
    ipgwLoginURL = "http://ipgw.neu.edu.cn/srun_portal_pc.php?ac_id=1&"
    ipgwInfoURL = "http://ipgw.neu.edu.cn/include/auth_action.php?k=23092"
    ipgwLogOutURL = "http://ipgw.neu.edu.cn/include/auth_action.php"

    def __init__(self, stuid, passwd):
        self.__stuId = stuid
        self.__password = passwd
        self.__login_data = {
            "action": "login",
            "ac_id": "1",
            "user_ip": "",
            "nas_ip": "",
            "user_mac": "",
            "url": "",
            "username": self.__stuId,
            "password": self.__password,
            "save_me": "0",
        }
        self.__info_data = {
            "action": "get_online_info",
            "key": "23092",
        }

        self.__logout_data = {
            "action": "logout",
            "username": self.__stuId,
            "password": self.__password,
            "ajax": "1",
        }

    def __str__(self):
        info_str = "A class serve to log-in"
        return info_str

    @property
    def getStuId(self):
        """Return the object's id."""
        return self.__stuId

    @property
    def getpassword(self):
        """Return the object's password."""
        return self.__password

    def getinfo(self):
        """Login,return empty dictionary when failed, return information dictionary when succeed"""
        self.logout()
        try:
            login_page = requests.post(self.ipgwLoginURL, self.__login_data)
        except:
            return {}
        else:
            if "已欠费" in login_page.text:
                return {}
        get_info = requests.post(self.ipgwInfoURL, self.__info_data)
        if "not_online" in get_info.text:
            return {}
        info_list = get_info.text.split(",")
        byte = int(info_list[0])
        time_s = int(info_list[1])
        balance = float(info_list[2])
        ip = info_list[5]
        gb = byte / (1024 * 1024 * 1024)
        hour = int(time_s / 3600)
        minute = int((time_s - hour * 3600) / 60)
        second = int(time_s - hour * 3600 - minute * 60)
        time = {
            "hour": hour,
            "minute": minute,
            "second": second,
        }
        return {
            "traffic": gb,
            "time": time,
            "balance": balance,
            "ip": ip,
        }

    def logout(self):
        """Log out from ipgw."""
        try:
            requests.post(self.ipgwLogOutURL, self.__logout_data)
        except:
            return 0
        return 1


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(624, 318)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.loginButton = QtWidgets.QPushButton(Form)
        self.loginButton.setGeometry(QtCore.QRect(80, 250, 112, 34))
        self.loginButton.setFlat(False)
        self.loginButton.setObjectName("loginButton")
        self.quitButton = QtWidgets.QPushButton(Form)
        self.quitButton.setGeometry(QtCore.QRect(420, 250, 112, 34))
        self.quitButton.setObjectName("quitButton")
        self.idEdit = QtWidgets.QLineEdit(Form)
        self.idEdit.setGeometry(QtCore.QRect(120, 73, 191, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        self.idEdit.setFont(font)
        self.idEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.idEdit.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.idEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.idEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.idEdit.setClearButtonEnabled(True)
        self.idEdit.setObjectName("idEdit")
        self.idEdit.setText(username)
        self.passwordEdit = QtWidgets.QLineEdit(Form)
        self.passwordEdit.setGeometry(QtCore.QRect(120, 130, 191, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(8)
        self.passwordEdit.setFont(font)
        self.passwordEdit.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhLatinOnly|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.passwordEdit.setText(password)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setClearButtonEnabled(True)
        self.passwordEdit.setObjectName("passwordEdit")
        self.idLabel = QtWidgets.QLabel(Form)
        self.idLabel.setGeometry(QtCore.QRect(40, 80, 54, 18))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        self.idLabel.setFont(font)
        self.idLabel.setTextFormat(QtCore.Qt.AutoText)
        self.idLabel.setObjectName("idLabel")
        self.passwordLabel = QtWidgets.QLabel(Form)
        self.passwordLabel.setGeometry(QtCore.QRect(40, 140, 45, 18))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")
        self.resultLabel = QtWidgets.QLabel(Form)
        self.resultLabel.setGeometry(QtCore.QRect(150, 170, 81, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.resultLabel.setFont(font)
        self.resultLabel.setText("")
        self.resultLabel.setObjectName("resultLabel")
        self.logoutButton = QtWidgets.QPushButton(Form)
        self.logoutButton.setGeometry(QtCore.QRect(250, 250, 112, 34))
        self.logoutButton.setFlat(False)
        self.logoutButton.setObjectName("logoutButton")
        self.infoFrame = QtWidgets.QFrame(Form)
        self.infoFrame.setGeometry(QtCore.QRect(320, 40, 291, 191))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.infoFrame.setFont(font)
        self.infoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.infoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.infoFrame.setObjectName("infoFrame")
        self.trafficLabel = QtWidgets.QLabel(self.infoFrame)
        self.trafficLabel.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.trafficLabel.setObjectName("trafficLabel")
        self.timeLabel = QtWidgets.QLabel(self.infoFrame)
        self.timeLabel.setGeometry(QtCore.QRect(10, 50, 81, 20))
        self.timeLabel.setObjectName("timeLabel")
        self.balanceLabel = QtWidgets.QLabel(self.infoFrame)
        self.balanceLabel.setGeometry(QtCore.QRect(10, 90, 81, 21))
        self.balanceLabel.setObjectName("balanceLabel")
        self.ipLabel = QtWidgets.QLabel(self.infoFrame)
        self.ipLabel.setGeometry(QtCore.QRect(10, 130, 81, 21))
        self.ipLabel.setObjectName("ipLabel")
        self.trafficEdit = QtWidgets.QLineEdit(self.infoFrame)
        self.trafficEdit.setGeometry(QtCore.QRect(110, 10, 141, 25))
        self.trafficEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.trafficEdit.setReadOnly(True)
        self.trafficEdit.setObjectName("trafficEdit")
        self.timeEdit = QtWidgets.QLineEdit(self.infoFrame)
        self.timeEdit.setGeometry(QtCore.QRect(110, 50, 141, 25))
        self.timeEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.timeEdit.setReadOnly(True)
        self.timeEdit.setObjectName("timeEdit")
        self.balanceEdit = QtWidgets.QLineEdit(self.infoFrame)
        self.balanceEdit.setGeometry(QtCore.QRect(110, 90, 141, 25))
        self.balanceEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.balanceEdit.setReadOnly(True)
        self.balanceEdit.setObjectName("balanceEdit")
        self.ipEdit = QtWidgets.QLineEdit(self.infoFrame)
        self.ipEdit.setGeometry(QtCore.QRect(110, 130, 141, 25))
        self.ipEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.ipEdit.setReadOnly(True)
        self.ipEdit.setObjectName("ipEdit")
        self.gbLabel = QtWidgets.QLabel(self.infoFrame)
        self.gbLabel.setGeometry(QtCore.QRect(250, 10, 31, 18))
        self.gbLabel.setObjectName("gbLabel")
        self.yuanLabel = QtWidgets.QLabel(self.infoFrame)
        self.yuanLabel.setGeometry(QtCore.QRect(250, 90, 31, 18))
        self.yuanLabel.setObjectName("yuanLabel")

        self.retranslateUi(Form)
        self.loginButton.clicked.connect(slotLogin)
        self.logoutButton.clicked.connect(slotLogout)
        self.quitButton.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.idEdit, self.passwordEdit)
        Form.setTabOrder(self.passwordEdit, self.loginButton)
        Form.setTabOrder(self.loginButton, self.logoutButton)
        Form.setTabOrder(self.logoutButton, self.quitButton)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "登陆"))
        self.loginButton.setToolTip(_translate("Form", "点击登陆"))
        self.loginButton.setText(_translate("Form", "登陆"))
        self.quitButton.setToolTip(_translate("Form", "关闭窗口"))
        self.quitButton.setText(_translate("Form", "关闭"))
        self.idEdit.setToolTip(_translate("Form", "<html><head/><body><p>在这里输入用户名</p></body></html>"))
        self.passwordEdit.setToolTip(_translate("Form", "<html><head/><body><p>在这里输入密码</p></body></html>"))
        self.idLabel.setText(_translate("Form", "用户名"))
        self.passwordLabel.setText(_translate("Form", "密 码"))
        self.logoutButton.setToolTip(_translate("Form", "点击注销"))
        self.logoutButton.setText(_translate("Form", "注销"))
        self.trafficLabel.setText(_translate("Form", "已用流量"))
        self.timeLabel.setText(_translate("Form", "已用时长"))
        self.balanceLabel.setText(_translate("Form", "账户余额"))
        self.ipLabel.setText(_translate("Form", "IP地址"))
        self.trafficEdit.setToolTip(_translate("Form", "已用流量"))
        self.timeEdit.setToolTip(_translate("Form", "已用时长"))
        self.balanceEdit.setToolTip(_translate("Form", "账户余额"))
        self.ipEdit.setToolTip(_translate("Form", "IP地址"))
        self.gbLabel.setText(_translate("Form", "Gb"))
        self.yuanLabel.setText(_translate("Form", "元"))


def slotLogin():
    window.resultLabel.setText("登陆中")
    loginObject = Login(window.idEdit.text(), window.passwordEdit.text())
    result = loginObject.getinfo()
    if result :
        hour = result["time"]["hour"]
        minute = result["time"]["minute"]
        second = result["time"]["second"]
        window.resultLabel.setText("登陆成功")
        window.trafficEdit.setText("{:.2f}".format(result["traffic"]))
        window.timeEdit.setText("{h}:{m}:{s}".format(h=hour, m=minute, s=second))
        window.balanceEdit.setText(str(result["balance"]))
        window.ipEdit.setText(result["ip"])
    else:
        window.resultLabel.setText("登陆失败")
        window.trafficEdit.setText("")
        window.timeEdit.setText("")
        window.balanceEdit.setText("")
        window.ipEdit.setText("")


def slotLogout():
    window.resultLabel.setText("注销中")
    loginObject = Login(window.idEdit.text(), window.passwordEdit.text())
    if loginObject:
        window.resultLabel.setText("注销成功")
        window.trafficEdit.setText("")
        window.timeEdit.setText("")
        window.balanceEdit.setText("")
        window.ipEdit.setText("")
    else:
        window.resultLabel.setText("注销失败")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    window = Ui_Form()
    window.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
