#Import thư viện
from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMenuBar, QStatusBar
from PyQt6 import QtCore, QtGui, QtWidgets
from playsound import playsound
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt
from bardapi import Bard
from gtts import gTTS
import sys
import os

#Set các biến
#icon_path = "bard_icon.png"
global user, bard, apikey, listen, bard_api
user = ""
bard = ""
listen = 0
bard_api = Bard(token_from_browser=True, timeout=10)

#Thanh trượt (Chỉ cho bard)
class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(Qt.Alignment.AlignLeading | Qt.Alignment.AlignLeft | Qt.Alignment.AlignTop)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)
    def setText(self, text):
        self.label.setText(text)

#UI
class Ui_MainWindow(object):
    #Setup UI
    def setupUi(self, MainWindow):
        #Cài đặt cửa sổ
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(400, 565)
        #icon = QIcon(icon_path)
        #app.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #=================LINE INPUT=================
        #User input line
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(5, 535, 311, 25))
        self.lineEdit.setObjectName("lineEdit")

        #Api input line
        self.lineAPI = QLineEdit(self.centralwidget)
        self.lineAPI.setGeometry(QtCore.QRect(5, 570, 311, 25))
        self.lineAPI.setObjectName("lineAPI")

        #=================BUTTON=================
        #Send button
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(325, 535, 71, 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.user_text)

        #User speak button
        self.button_user_speak = QPushButton(self.centralwidget)
        self.button_user_speak.setGeometry(QtCore.QRect(5, 10, 25, 25))
        self.button_user_speak.setObjectName("button_user_speak")
        self.button_user_speak.clicked.connect(self.user_speak)

        #Bard speak button
        self.button_bard_speak = QPushButton(self.centralwidget)
        self.button_bard_speak.setGeometry(QtCore.QRect(5, 130, 25, 25))
        self.button_bard_speak.setObjectName("button_bard_speak")
        self.button_bard_speak.clicked.connect(self.bard_speak)

        #Bard export button
        self.button_export = QPushButton(self.centralwidget)
        self.button_export.setGeometry(QtCore.QRect(92, 130, 55, 25))
        self.button_export.setObjectName("button_export")
        self.button_export.clicked.connect(self.bard_export)

        #=================TEXT=================
        
        #Label 1 - You
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label = QLabel(self.centralwidget)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(35, 10, 51, 21))
        
        #Label 2 - Bard
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(35, 130, 51, 21))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 391, 81))

        #Label 3 - User Input
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_3.setAlignment(Qt.Alignment.AlignLeading | Qt.Alignment.AlignLeft | Qt.Alignment.AlignTop)
        self.label_3.setObjectName("label_3")

        #Label 4 - Bard answer
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4 = ScrollLabel(self.centralwidget)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_4.setAlignment(Qt.Alignment.AlignLeading | Qt.Alignment.AlignLeft | Qt.Alignment.AlignTop)
        self.label_4.setObjectName("label_4")
        #Scoll bar cho label 4
        self.label_4.setGeometry(QtCore.QRect(0, 160, 400, 341))
        self.label_4.verticalScrollBar().setStyleSheet("QScrollBar:vertical { border: none; }")
        self.label_4.setStyleSheet("QScrollArea { border: none; }")
        
        #Hàm lấy chữ cho các widget
        self.retranslateUi(MainWindow)

    #Translate UI
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        #==Window Title==
        MainWindow.setWindowTitle(_translate("MainWindow", "Bard"))

        #=====BUTTON=====
        self.button_bard_speak.setText(_translate("MainWindow", "🔊"))
        self.button_user_speak.setText(_translate("MainWindow", "🔊"))
        self.button_export.setText(_translate("MainWindow", "Export"))
        self.pushButton.setText(_translate("MainWindow", "Send"))
        
        #=====TEXT-LB=====
        self.label.setText(_translate("MainWindow", "You"))
        self.label_2.setText(_translate("MainWindow", "Bard"))
        self.label_3.setText(_translate("MainWindow", user))
        self.label_3.setWordWrap(True)
        self.label_4.setText(_translate("MainWindow", bard))

    #Export to "answer.txt"
    def bard_export(self):
        export_file = "You: " + user + "\nBard: " + bard
        with open("answer.txt", "w") as f:
            f.write(export_file)

    #Lấy kết quả từ bard
    def user_text(self):
        global user, bard
        user = self.lineEdit.text()
        self.label_3.setText(user)
        if bard_api == "" or user == "":
            bard = "Không đủ thông tin đầu vào"
            self.label_3.setText(user)
            tts = gTTS(user, lang='vi', slow = False)
            tts.save('user.mp3')
            self.label_4.setText(bard)
            tts = gTTS(bard, lang='vi', slow = False)
            tts.save('bard.mp3')
        elif len(user) > 0:
            user_input = user.strip()
            if len(user_input) == 0:
                pass
            elif len(user_input) > 0:
                QApplication.processEvents()
                app.quitOnLastWindowClosed = False
                bard = bard_api.get_answer(user)['content']
                QApplication.processEvents()
                self.label_3.setText(user)
                tts = gTTS(user, lang='vi', slow = False)
                tts.save('user.mp3')

                self.label_4.setText(bard)
                tts = gTTS(bard, lang='vi', slow = False)
                tts.save('bard.mp3')

    #Nói user input
    def user_speak(self):
        global listen
        if listen == 0:
            listen = 1
            self.button_user_speak.setText("⏹")
            playsound('user.mp3')
            self.button_user_speak.setText("🔊")
            listen = 0
        if listen == 1:
            pass

    #Nói bard answer
    def bard_speak(self):
        global listen
        if listen == 0:
            listen += 1
            playsound('bard.mp3')
            listen = 0
        elif listen == 1:
            pass

#Vòng lặp chương trình
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
