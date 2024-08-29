import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGraphicsBlurEffect, QGraphicsDropShadowEffect, QLabel, QPlainTextEdit
from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import QCoreApplication, Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer, QSequentialAnimationGroup, QEventLoop, QTimer
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QFontDatabase, QFont, QTextLine
from qframelesswindow import FramelessWindow, AcrylicWindow
from win32api import GetSystemMetrics
import math
import time
from pystray import MenuItem as item
import pystray
from PIL import Image
import Alice_LM
import nonAIinputProcess

#Make sure putting OAI API key at 'ALICE_LM.py'.
#Adjust scale. default = 1, will not work properly.
scale = 1

def relWidth(width):
    return round(float(width) * float(scale))
def relHeight(height):
    return round(float(height) * float(scale))
class WorkerThread(QtCore.QObject):
    signalExample = QtCore.pyqtSignal(str, int)
    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            self.signalExample.emit("run", 1)
            time.sleep(1)


class Main(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI() 

    def signalExample(self, text, number):
        print(text)
        print(number)
    def systray_action():
       pass

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)  
    
    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
    
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event) 

    def initUI(self):
        self.worker = WorkerThread()
        self.workerThread = QtCore.QThread()
        self.workerThread.started.connect(self.worker.run)
        self.worker.signalExample.connect(self.signalExample)
        self.worker.moveToThread(self.workerThread)
        self.move(500, -500)
        self.setWindowTitle('Alice')
        self.setWindowIcon(QtGui.QIcon('Alice\\icons\\ALice_icon.png'))
        self.resize(relHeight(451), relHeight(760))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.blur_effect = QGraphicsBlurEffect()
        self.inputbox_shadow_effect = QGraphicsDropShadowEffect()
        self.enterButton_shadow_effect = QGraphicsDropShadowEffect()
        #Main Window
        
        self.main_window = self.main_window = QWidget(self)
        self.main_window.resize(relWidth(450), relHeight(150))
        self.main_window.move(0, relHeight(750) - relHeight(160))
        self.main_window.setStyleSheet(
            """
            background: rgba(115, 115, 115, 0.5);
            background: qlineargradient(spread: ppad, x1:0, y1:0, x2:0, y2:1 stop:0 #575757, stop:1 #494949);
            border-radius: """ + str(relWidth(35)) + """px;
            border: 2px solid #676767;
            
            """
        )
        
        self.button_desk = QWidget(self.main_window)
        self.button_desk.resize(relWidth(60), relHeight(30))
        self.button_desk.move((relWidth(450) - relWidth(75)), relHeight(10))
        self.button_desk.setStyleSheet("background: #000000;border-radius: " + str(relWidth(14.95)) +"px;border: 2px #ffffff;")

        self.minimizeButton = QWidget(self.button_desk)
        self.minimizeButton.setStyleSheet("background: #ffffff; border-radius: " + str(relWidth(12)) + ";")
        self.minimizeButton.resize(relWidth(24), relHeight(24))
        self.minimizeButton.move(relWidth(34), relHeight(3.255))

        self.minimizeIcon = QLabel(self.button_desk)
        self.minimizeIcon.setPixmap(QtGui.QPixmap("Alice\\icons\\minimize.png"))
        self.minimizeIcon.resize(relWidth(20), relHeight(20))
        self.minimizeIcon.setScaledContents(True)
        self.minimizeIcon.move(relWidth(35.5), relHeight(5.255))
        self.minimizeIcon.setStyleSheet("background: rgba(255, 255, 255, 0)")
        self.minimizeIcon.show()

        self.minimizeButtonReal = QPushButton(self.button_desk)
        self.minimizeButtonReal.setStyleSheet("background: rgba(0, 0, 0, 0); border-radius: " + str(relWidth(12)) + ";")
        self.minimizeButtonReal.resize(relWidth(24), relHeight(24))
        self.minimizeButtonReal.move(relWidth(34), relHeight(3.255))
        self.minimizeButtonReal.clicked.connect(QApplication.instance().quit )

        self.settingsButton = QWidget(self.button_desk)
        self.settingsButton.setStyleSheet("background: #ffffff; border-radius: " + str(relWidth(12)) + ";")
        self.settingsButton.resize(relWidth(24), relHeight(24))
        self.settingsButton.move(relWidth(3), relHeight(3.255))    

        self.settingsIcon = QLabel(self.button_desk)
        self.settingsIcon.setPixmap(QtGui.QPixmap("Alice\\icons\\settings.png"))
        self.settingsIcon.resize(relWidth(20), relHeight(20))
        self.settingsIcon.setScaledContents(True)
        self.settingsIcon.move(relWidth(4.7), relHeight(5.255))
        self.settingsIcon.setStyleSheet("background: rgba(255, 255, 255, 0)")
        self.settingsIcon.show()

        self.settingsButtonReal = QPushButton(self.button_desk)
        self.settingsButtonReal.setStyleSheet("background: rgba(0, 0, 0, 0); border-radius: " + str(relWidth(12)) + ";")
        self.settingsButtonReal.resize(relWidth(24), relHeight(24))
        self.settingsButtonReal.move(relWidth(3), relHeight(3.255))
        self.settingsButtonReal.clicked.connect(self.settingspanel)
        #Input Box.
        self.input_background = QWidget(self.main_window)
        self.input_background.resize(relWidth(365), relHeight(90))
        self.input_background.move(relWidth(10), (relHeight(150) - relHeight(100)))
        self.input_background.setStyleSheet("Background: qlineargradient(spread: ppad, x1:0, y1:0, x2:0, y2:1 stop:0 #9f9f9f, stop:1 #7f7f7f); border: 2px solid #9f9f9f;")
        self.inputbox_shadow_effect.setColor(QColor(50, 50, 50))
        self.inputbox_shadow_effect.setOffset(3, 3)
        self.inputbox_shadow_effect.setBlurRadius(10)
        self.input_background.setGraphicsEffect(self.inputbox_shadow_effect)

        self.input_textbox = QPlainTextEdit(self.main_window)
        self.input_textbox.resize(relWidth(325), relHeight(70))
        self.input_textbox.setStyleSheet("border-radius: 0px; background-color: rgba(255, 255, 255, 0); border: none; color: #373351; font-size: " + str(relHeight(22)) + "px; font-weight: bold")
        self.input_textbox.move(relWidth(30), (relHeight(150) - relHeight(91)))

        self.chatlistbackground = QWidget(self.main_window)
        self.chatlistbackground.resize(relWidth(35), relHeight(35))
        self.chatlistbackground.move((relWidth(450) - relWidth(435)), relHeight(7))
        self.chatlistbackground.setStyleSheet("background: #000000;border-radius: " + str(relWidth(16.7)) +"px;border: 2px #ffffff;")

        
        self.chaticon = QLabel(self.main_window)
        self.chaticon.setPixmap(QtGui.QPixmap("Alice\\icons\\chaticon.png"))
        self.chaticon.resize(relWidth(26), relHeight(26))
        self.chaticon.setScaledContents(True)
        self.chaticon.setStyleSheet("background: rgba(255, 255, 255, 0); border:none;")
        self.chaticon.move((relWidth(450) - relWidth(430)), relHeight(12))
        self.chaticon.show()

        self.enterButton = QWidget(self.main_window)
        self.enterButton.resize(relWidth(60), relHeight(90))
        self.enterButton.move((relWidth(450) - relWidth(70)), (relHeight(150) - relHeight(100)))
        self.enterButton.setStyleSheet("border-radius: " + str(relWidth(30.5)) + "px; border: 1px none; background: #246DFF; border: 1px solid #3C7DFF;")
        self.enterButton_shadow_effect.setColor(QColor(21, 100, 255))
        self.enterButton_shadow_effect.setOffset(-1, -1)
        self.enterButton_shadow_effect.setBlurRadius(10)
        self.enterButton.setGraphicsEffect(self.enterButton_shadow_effect)

        self.enterIcon = QLabel(self.main_window)
        self.enterIcon.setPixmap(QtGui.QPixmap("Alice\\icons\\Enter.png"))
        self.enterIcon.resize(relWidth(40), relHeight(40))
        self.enterIcon.setScaledContents(True)
        self.enterIcon.setStyleSheet("background: rgba(255, 255, 255, 0); border:none;")
        self.enterIcon.move((relWidth(450) - relWidth(60)), (relHeight(150) - relHeight(75)))
        self.enterIcon.show()

        self.enterButtonReal = QPushButton(self.main_window)
        self.enterButtonReal.setStyleSheet("background: rgba(0, 0, 0, 0); border-radius: " + str(relWidth(30.5)) + ";")
        self.enterButtonReal.resize(relWidth(60), relHeight(90))
        self.enterButtonReal.move((relWidth(450) - relWidth(70)), (relHeight(150) - relHeight(100)))
        self.enterButtonReal.clicked.connect(self.enterButtonPress)

        self.dynamicwidget = QWidget(self)
        self.dynamicwidget.resize(relWidth(200), relHeight(35))
        self.dynamicwidget.move((relWidth(450) - relWidth(335)), relHeight(597))
        self.dynamicwidget.setStyleSheet("background: #000000;border-radius: " + str(relWidth(16.7)) +"px;border: 2px #ffffff;")

        self.chatBox = QPlainTextEdit(self)
        self.chatBox.resize(relWidth(150), relHeight(35))
        self.chatBox.move((relWidth(450) - relWidth(310)), relHeight(597))
        self.chatBox.setStyleSheet("background: #000000;border-radius: " + str(relWidth(19)) +"px;")
               
        self.chatBoxExpansionState = "none"
        self.chatBoxinitialWidth = relWidth(150)
        self.chatBoxinitialHeight = relHeight(35)
        self.chatboxinitialX = relWidth(450) - relWidth(310)
        self.chatboxinitialY = relHeight(597)

        self.chatBoxLabel = QLabel(self.chatBox)
        self.chatBoxLabel.resize(relWidth(400), relHeight(50))
        self.chatBoxLabel.setStyleSheet("background: rgba(255, 255, 255, 0); color: #ffffff; border-radius: none; font-size: " + str(relHeight(15)) + "px;")
        self.chatBoxLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.chatBoxLabel.move(relWidth(20), relHeight(10))
        
        self.textBlur = QGraphicsDropShadowEffect()
        self.textBlur.setBlurRadius(25)
        self.textBlur.setColor(QColor(255, 255, 255))
        self.textBlur.setOffset(0, 0)
        self.chatBoxLabel.setGraphicsEffect(self.textBlur)

        self.answerBoxLabel = QLabel(self.chatBox)
        self.answerBoxLabel.resize(relWidth(400), relHeight(50))
        self.answerBoxLabel.setStyleSheet("background: rgba(255, 255, 255, 0); color: #ffffff; border-radius: none; font-size: " + str(relHeight(15)) + "px;")
        self.answerBoxLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.answerBoxLabel.move(relWidth(20), relHeight(-50))
        self.answerBoxLabel.setWordWrap(True)
        
        self.messages = []

        self.chatStatus = "none"
        self.show()

    def chatBoxExpansion(self, event, origin, target):
        self.chatBoxAnimation = QPropertyAnimation(self.chatBox, b"geometry")
        if origin == "none":   
            self.chatBoxAnimation.setStartValue(QRect(self.chatboxinitialX, self.chatboxinitialY, self.chatBoxinitialWidth, self.chatBoxinitialHeight))

        elif origin == "small":
            ymovebalue = round(self.chatboxinitialY - relHeight(35) - relHeight(55))
            self.chatBoxAnimation.setStartValue(QRect(relWidth(10), ymovebalue, relWidth(430), (self.chatBoxinitialHeight + relHeight(35))))
        
        elif origin == "medium":
            ymovebalue = round(self.chatboxinitialY - relHeight(100) - relHeight(55))
            self.chatBoxAnimation.setStartValue(QRect(relWidth(10), ymovebalue, relWidth(430), (self.chatBoxinitialHeight + relHeight(100))))
        elif origin == "large":
            ymovebalue = round(self.chatboxinitialY - relHeight(300) - relHeight(55))
            self.chatBoxAnimation.setStartValue(QRect(relWidth(10), ymovebalue, relWidth(430), (self.chatBoxinitialHeight + relHeight(300))))
        
        if target == "none":
            self.chatBoxAnimation.setDuration(700)
            self.chatBoxAnimation.setEndValue(QRect(self.chatboxinitialX, self.chatboxinitialY, self.chatBoxinitialWidth, self.chatBoxinitialHeight))
            self.chatBoxAnimation.setEasingCurve(QEasingCurve.Type.InBack)
            self.chatBoxAnimation.start()
            self.chatBoxExpansionState = "none"
        
        elif target == "small":
            self.chatBoxAnimation.setDuration(700)
            ymovebalue = round(self.chatboxinitialY - relHeight(35) - relHeight(55))
            self.chatBoxAnimation.setEndValue(QRect(relWidth(10), ymovebalue, relWidth(430), (self.chatBoxinitialHeight + relHeight(35))))
            self.chatBoxAnimation.setEasingCurve(QEasingCurve.Type.OutBack)
            self.chatBoxAnimation.start()
            self.chatBoxExpansionState = "small"
        
        elif target == "medium":
            self.chatBoxAnimation.setDuration(800)
            ymovebalue = round(self.chatboxinitialY - relHeight(100) - relHeight(55))
            self.chatBoxAnimation.setEndValue(QRect(relWidth(10), ymovebalue, relWidth(430), (self.chatBoxinitialHeight + relHeight(100))))
            self.chatBoxAnimation.setEasingCurve(QEasingCurve.Type.OutBack)
            self.chatBoxAnimation.start()
            self.chatBoxExpansionState = "medium"
        
        elif target == "large":
            self.chatBoxAnimation.setDuration(800)
            ymovebalue = round(self.chatboxinitialY - relHeight(300) - relHeight(55))
            self.chatBoxAnimation.setEndValue(QRect(relWidth(10), ymovebalue, relWidth(430), (self.chatBoxinitialHeight + relHeight(300))))
            self.chatBoxAnimation.setEasingCurve(QEasingCurve.Type.OutBack)
            self.chatBoxAnimation.start()
            self.chatBoxExpansionState = "large"

    def labelUp(self, event):
        self.chatBoxLabel.move(relWidth(25), relHeight(70))
        self.chatBoxLabelAnimation = QPropertyAnimation(self.chatBoxLabel, b"geometry")
        self.chatBoxLabelAnimation.setStartValue(QRect(relWidth(20), relHeight(70), relWidth(400), relHeight(50)))
        self.chatBoxLabelAnimation.setEndValue(QRect(relWidth(20), relHeight(10), relWidth(400), relHeight(50)))
        self.chatBoxLabelAnimation.setDuration(500)
        self.chatBoxLabelAnimation.start()
        self.wait(2000)
    

    def answerLabelDown(self, event):
        self.answerBoxLabel.move(relWidth(25), relHeight(-50))
        self.answerBoxLabelAnimation = QPropertyAnimation(self.answerBoxLabel, b"geometry")
        self.answerBoxLabelAnimation.setStartValue(QRect(relWidth(20), relHeight(-50), relWidth(400), relHeight(50)))
        self.answerBoxLabelAnimation.setEndValue(QRect(relWidth(20), relHeight(10), relWidth(400), relHeight(50)))
        self.answerBoxLabelAnimation.setDuration(500)
        self.answerBoxLabelAnimation.start()


    def wait(self, msecs):
        loop = QEventLoop()
        QTimer.singleShot(msecs, loop.quit)

    def enterButtonPress(self, event):
        input = self.input_textbox.toPlainText()
        self.textBlur = QGraphicsDropShadowEffect()
        self.textBlur.setBlurRadius(15)
        self.textBlur.setColor(QColor(255, 255, 255))
        self.textBlur.setOffset(0, 0)
        self.answerBoxLabel.setGraphicsEffect(self.textBlur)
        
        
        
        self.messages.append({"role": "user", "content": input})
        responce = Alice_LM.alice_ai_chat(self.messages)
            
        self.messages.append({"role": "assistant", "content": responce})
        self.answerBoxLabel.setText("Alice | " + responce)
        if input == "대화 끝내줘":
            self.answerBoxLabel.setText("")
            self.chatBoxExpansion(self, self.chatBoxExpansionState, "none")
            self.input_textbox.setPlainText("")
            return
        v = 0
        for i in responce:
            v = v + 1
        
        print(v)
        if v < 70:
            self.chatBoxExpansion(self, self.chatBoxExpansionState, "small")    
            self.answerBoxLabel.setFixedHeight(50)
        elif 69 < v < 180:
            self.chatBoxExpansion(self, self.chatBoxExpansionState, "medium")  
            self.answerBoxLabel.setFixedHeight(120)  
        elif v > 179:
            self.chatBoxExpansion(self, self.chatBoxExpansionState, "large")  
            self.answerBoxLabel.setFixedHeight(330)
            self.answerBoxLabel.scroll
        self.input_textbox.setPlainText("")
        
        self.answerLabelDown(self)


            
            

    def settingspanel(self, event):
        text, done = QtWidgets.QInputDialog.getText(self, '크기 조정', '크기를 입력(소수)')
        scale = float(text)
        Main.update(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())


