# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Sun Mar 30 22:34:44 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import playfulbot_core

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(327, 223)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 20, 191, 61))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("images/logo.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.loginEdit = QtGui.QLineEdit(Dialog)
        self.loginEdit.setGeometry(QtCore.QRect(30, 100, 271, 21))
        self.loginEdit.setObjectName(_fromUtf8("loginEdit"))
        self.passEdit = QtGui.QLineEdit(Dialog)
        self.passEdit.setGeometry(QtCore.QRect(30, 140, 271, 21))
        self.passEdit.setText(_fromUtf8(""))
        self.passEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passEdit.setObjectName(_fromUtf8("passEdit"))
        self.btnLogin = QtGui.QPushButton(Dialog)
        self.btnLogin.setGeometry(QtCore.QRect(190, 180, 114, 32))
        self.btnLogin.setObjectName(_fromUtf8("btnLogin"))
        self.btnLogin.clicked.connect(self.onClickLogin)
        bot.signalLogin.connect(self.loginResult)
        self.bot_thread = QtCore.QThread()
        bot.moveToThread(self.bot_thread)
        bot.signalLogin.connect(self.bot_thread.quit)
        self.bot_thread.started.connect(bot.login)

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
        self.bot_thread.start()

    def loginResult(self, connected):
        box = QtGui.QMessageBox(LoginDialog)
        box.setWindowModality(QtCore.Qt.WindowModal)
        if connected:
            box.setIcon(QtGui.QMessageBox.Information)
            box.setText("Bienvenido a Playfulbot")
        else:
            box.setIcon(QtGui.QMessageBox.Warning)
            box.setText("No se ha podido conectar")
        self.loginEdit.setEnabled(True)
        self.passEdit.setEnabled(True)
        self.btnLogin.setEnabled(True)
        box.show()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    LoginDialog = QtGui.QDialog()
    app.setActiveWindow(LoginDialog)
    bot = playfulbot_core.PlayfulbotCore()
    ui = Ui_Dialog()
    ui.setupUi(LoginDialog)
    LoginDialog.show()
    sys.exit(app.exec_())