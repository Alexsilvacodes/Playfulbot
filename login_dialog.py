# -*- coding: utf-8 -*-
#
# 2015 Alex Silva <alexsilvaf28 at gmail.com>

from PyQt4 import QtCore, QtGui
from main_window import *
import playfulbot_core, locale

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MyDialog(QtGui.QDialog):

    def __init__(self, parent=None, flags=QtCore.Qt.Dialog):
        super(MyDialog, self).__init__(parent, flags)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.setFocus()
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(327, 250)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(327, 250))
        Dialog.setMaximumSize(QtCore.QSize(327, 250))
        Dialog.setStyleSheet(_fromUtf8("QDialog{background-color: #092b39; color: white;}"))
        flags = QtCore.Qt.CustomizeWindowHint
        Dialog.setWindowFlags(flags)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 20, 191, 61))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("images/logo.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.loginEdit = QtGui.QLineEdit(Dialog)
        self.loginEdit.setGeometry(QtCore.QRect(30, 110, 271, 31))
        self.labelBGSpinner = QtGui.QLabel(Dialog)
        self.labelBGSpinner.setGeometry(QtCore.QRect(240, 20, 61, 61))
        self.labelBGSpinner.setText(_fromUtf8(""))
        self.labelBGSpinner.setObjectName(_fromUtf8("labelBGSpinner"))
        self.labelBGSpinner.setPixmap(QtGui.QPixmap(_fromUtf8("images/bgspinner.png")))
        self.labelSpinner = QtGui.QLabel(Dialog)
        self.spinner = QtGui.QMovie("images/spinner.gif")
        self.spinner.setScaledSize(QtCore.QSize(49, 39))
        self.labelSpinner.setGeometry(QtCore.QRect(248, 17, 61, 61))
        self.labelSpinner.setText(_fromUtf8(""))
        self.labelSpinner.setObjectName(_fromUtf8("labelSpinner"))
        self.labelSpinner.setMovie(self.spinner)
        self.spinner.start()
        self.labelSpinner.setVisible(False)
        self.labelBGSpinner.setVisible(False)
        self.loginEdit = QtGui.QLineEdit(Dialog)
        self.loginEdit.setGeometry(QtCore.QRect(30, 110, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.loginEdit.setFont(font)
        self.loginEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.loginEdit.setObjectName(_fromUtf8("loginEdit"))
        self.loginEdit.selectAll()
        self.loginEdit.setFocus()
        self.passEdit = QtGui.QLineEdit(Dialog)
        self.passEdit.setGeometry(QtCore.QRect(30, 160, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.passEdit.setFont(font)
        self.passEdit.setText(_fromUtf8(""))
        self.passEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.passEdit.setObjectName(_fromUtf8("passEdit"))
        self.btnLogin = QtGui.QPushButton(Dialog)
        self.btnLogin.setGeometry(QtCore.QRect(190, 205, 114, 32))
        self.btnLogin.setObjectName(_fromUtf8("btnLogin"))
        self.btnLogin.clicked.connect(self.onClickLogin)
        # Threads and signals
        bot.signalLogin.connect(self.setConnected)
        self.bot_thread = QtCore.QThread()
        bot.moveToThread(self.bot_thread)
        bot.signalLogin.connect(self.bot_thread.quit)
        self.bot_thread.started.connect(bot.login)
        self.bot_thread.finished.connect(self.loginResult)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Playfulbot", None))
        self.loginEdit.setPlaceholderText(_translate("Dialog", "Nombre usuario o email", None))
        self.passEdit.setPlaceholderText(_translate("Dialog", "Contraseña", None))
        self.btnLogin.setText(_translate("Dialog", "Entra", None))

    def onClickLogin(self):
        bot.setLogin(self.loginEdit.text())
        bot.setPassword(self.passEdit.text())
        self.loginEdit.setEnabled(False)
        self.passEdit.setEnabled(False)
        self.btnLogin.setEnabled(False)
        self.animation = QtCore.QPropertyAnimation(self.label, "geometry")
        self.animation.setDuration(800)
        self.animation.setStartValue(QtCore.QRect(70, 20, 191, 61))
        self.animation.setEndValue(QtCore.QRect(30, 20, 191, 61))
        self.animation.start()
        self.animation.finished.connect(lambda: self.labelBGSpinner.setVisible(True))
        self.animation.finished.connect(lambda: self.labelSpinner.setVisible(True))
        self.bot_thread.start()

    def setConnected(self, connected):
        self.connected = connected

    def loginResult(self):
        if self.connected:
            self.bot_thread.started.disconnect()
            self.bot_thread.finished.disconnect()
            bot.signalUserData.connect(self.bot_thread.quit)
            self.bot_thread.started.connect(bot.userData)
            self.bot_thread.finished.connect(LoginDialog.close)
            bot.signalUserData.connect(ui_mw.setUserData)
            LoginDialog.finished.connect(MainWindow.show)
            self.bot_thread.start()
        else:
            self.loginEdit.setText(_fromUtf8(""))
            self.passEdit.setText(_fromUtf8(""))
            self.loginEdit.setEnabled(True)
            self.passEdit.setEnabled(True)
            self.btnLogin.setEnabled(True)
            self.animation = QtCore.QPropertyAnimation(self.label, "geometry")
            self.animation.setDuration(75)
            self.animation.setStartValue(QtCore.QRect(30, 20, 191, 61))
            self.animation.setEndValue(QtCore.QRect(75, 20, 191, 61))
            self.animation1 = QtCore.QPropertyAnimation(self.label, "geometry")
            self.animation1.setDuration(75)
            self.animation1.setStartValue(QtCore.QRect(75, 20, 191, 61))
            self.animation1.setEndValue(QtCore.QRect(35, 20, 191, 61))
            self.animation2 = QtCore.QPropertyAnimation(self.label, "geometry")
            self.animation2.setDuration(75)
            self.animation2.setStartValue(QtCore.QRect(35, 20, 191, 61))
            self.animation2.setEndValue(QtCore.QRect(70, 20, 191, 61))
            self.secuentialAnimation = QtCore.QSequentialAnimationGroup()
            self.secuentialAnimation.addAnimation(self.animation)
            self.secuentialAnimation.addAnimation(self.animation1)
            self.secuentialAnimation.addAnimation(self.animation2)
            self.secuentialAnimation.start()
            self.labelBGSpinner.setVisible(False)
            self.labelSpinner.setVisible(False)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui_mw = Ui_MainWindow(MainWindow)
    LoginDialog = MyDialog()
    app.setActiveWindow(LoginDialog)
    bot = playfulbot_core.PlayfulbotCore()
    ui_login = Ui_Dialog()
    ui_login.setupUi(LoginDialog)
    LoginDialog.show()
    sys.exit(app.exec_())
