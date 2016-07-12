# -*- coding: utf-8 -*-
#
# 2014 Alex Silva <alexsilvaf28 at gmail.com>

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(QtCore.QObject):

    def __init__(self, main_window):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(main_window)

    def setUserData(self, data):
        self.data = data
        level_colors = {
            "blue": "#21a4d8",
            "green": "#2fc2a2",
            "red": "#db6436",
            "lilac": "#7d5ec7",
            "gold": "#dfb14f"
        }
        photo_pix = QtGui.QPixmap.fromImage(QtGui.QImage.fromData(self.data['userimage'])).scaled(122, 122)
        if photo_pix.isNull():
            photo_pix.load("images/default.jpg")
        self.photo_label.setPixmap(photo_pix)

        if int(self.data['level']) < 16:
            level_color = level_colors["blue"]
        elif int(self.data['level']) < 31:
            level_color = level_colors["green"]
        elif int(self.data['level']) < 51:
            level_color = level_colors["red"]
        elif int(self.data['level']) < 71:
            level_color = level_colors["lilac"]
        else:
            level_color = level_colors["gold"]
        self.frame_photo.setStyleSheet(_fromUtf8("QFrame {\
        background-color: transparent;\
        border-bottom-color: " + level_color + ";\
        border-bottom-left-radius: 60%;\
        border-bottom-right-radius: 60%;\
        border-bottom-style: solid;\
        border-bottom-width: 4px;\
        border-left-color: " + level_color + ";\
        border-left-style: solid;\
        border-left-width: 4px;\
        border-right-color: " + level_color + ";\
        border-right-style: solid;\
        border-right-width: 4px;\
        border-top-color: " + level_color + ";\
        border-top-left-radius: 60%;\
        border-top-right-radius: 60%;\
        border-top-style: solid;\
        border-top-width: 4px;}"))
        self.photo_label.setMask(QtGui.QPixmap("images/profile_frame.png").mask())

        self.user_label.setText(self.data['username'])
        self.coins_label.setText(self.data['activecoins'])
        self.coins_p_label.setText(self.data['playedcoins'])
        self.level_label.setText("Nivel " + self.data['level'])
        self.level_progress.setValue(float(self.data['levelbar']))
        self.played_label.setText(self.data['playedtotal'] + " jugadas")

        self.tab_widget.setTabText(self.tab_widget.indexOf(self.pend_tab), _translate("MainWindow", "0" + " Pendientes", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.win_tab), _translate("MainWindow", self.data['wins'] + " Ganadas", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.lost_tab), _translate("MainWindow", self.data['lost'] +" Perdidas", None))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1024, 768)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 768))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 768))
        x = (QtGui.QApplication.desktop().width() - 1024) / 2
        y = (QtGui.QApplication.desktop().height() - 768) / 2
        MainWindow.move(x, y)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(_fromUtf8("QWidget{background-color: white;}"))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame_left = QtGui.QFrame(self.centralwidget)
        self.frame_left.setGeometry(QtCore.QRect(0, 0, 1024, 144))
        self.frame_left.setStyleSheet(_fromUtf8("QFrame {background-color: #092b39; color: white;}"))
        self.frame_left.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_left.setObjectName(_fromUtf8("frame_left"))
        self.user_label = QtGui.QLabel(self.frame_left)
        self.user_label.setGeometry(QtCore.QRect(160, 20, 211, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Helvetica Neue"))
        font.setPointSize(29)
        self.photo_label = QtGui.QLabel(self.frame_left)
        self.photo_label.setGeometry(QtCore.QRect(10, 10, 122, 122))
        self.photo_label.setObjectName(_fromUtf8("photo_label"))
        self.photo_label.setStyleSheet(_fromUtf8("QFrame {border: transparent 4px;}"))
        self.frame_photo = QtGui.QFrame(self.frame_left)
        self.frame_photo.setGeometry(QtCore.QRect(10, 10, 122, 122))
        self.user_label.setFont(font)
        self.user_label.setStyleSheet(_fromUtf8("QLabel { color: white; }"))
        self.user_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.user_label.setObjectName(_fromUtf8("user_label"))
        self.label = QtGui.QLabel(self.frame_left)
        self.label.setGeometry(QtCore.QRect(870, 30, 65, 31))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("QLabel{color: #21a4d8}"))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.frame_left)
        self.label_2.setGeometry(QtCore.QRect(860, 80, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(_fromUtf8("QLabel{color: #21a4d8}"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.coins_p_label = QtGui.QLabel(self.frame_left)
        self.coins_p_label.setGeometry(QtCore.QRect(670, 80, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.coins_p_label.setFont(font)
        self.coins_p_label.setStyleSheet(_fromUtf8("QLabel{color: #ff7010}"))
        self.coins_p_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.coins_p_label.setObjectName(_fromUtf8("coins_p_label"))
        self.coins_label = QtGui.QLabel(self.frame_left)
        self.coins_label.setGeometry(QtCore.QRect(660, 30, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.coins_label.setFont(font)
        self.coins_label.setStyleSheet(_fromUtf8("QLabel{color: #3bbc75}"))
        self.coins_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.coins_label.setObjectName(_fromUtf8("coins_label"))
        self.level_progress = QtGui.QProgressBar(self.frame_left)
        self.level_progress.setGeometry(QtCore.QRect(370, 90, 281, 23))
        self.level_progress.setProperty("value", 0)
        self.level_progress.setTextVisible(False)
        self.level_progress.setObjectName(_fromUtf8("level_progress"))
        self.level_progress.setStyleSheet("QProgressBar { border: 3px transparent; border-radius: 7px; background-color: #105069;} \
        QProgressBar::chunk { background-color: #21a4d8;border-radius: 5px; }");
        self.level_label = QtGui.QLabel(self.frame_left)
        self.level_label.setGeometry(QtCore.QRect(370, 59, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.level_label.setFont(font)
        self.level_label.setAlignment(QtCore.Qt.AlignCenter)
        self.level_label.setObjectName(_fromUtf8("level_label"))
        self.played_label = QtGui.QLabel(self.frame_left)
        self.played_label.setGeometry(QtCore.QRect(160, 70, 161, 26))
        self.played_label.setObjectName(_fromUtf8("played_label"))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.played_label.setFont(font)
        self.tab_widget = QtGui.QTabWidget(self.centralwidget)
        self.tab_widget.setGeometry(QtCore.QRect(10, 150, 1002, 587))
        self.tab_widget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tab_widget.setObjectName(_fromUtf8("tab_widget"))
        self.pend_tab = QtGui.QWidget()
        self.pend_tab.setObjectName(_fromUtf8("pend_tab"))
        self.pend_table_view = QtGui.QTableView(self.pend_tab)
        self.pend_table_view.setGeometry(QtCore.QRect(0, 0, 996, 558))
        self.pend_table_view.setFrameShape(QtGui.QFrame.NoFrame)
        self.pend_table_view.setGridStyle(QtCore.Qt.NoPen)
        self.pend_table_view.setObjectName(_fromUtf8("pend_table_view"))
        self.tab_widget.addTab(self.pend_tab, _fromUtf8(""))
        self.win_tab = QtGui.QWidget()
        self.win_tab.setObjectName(_fromUtf8("win_tab"))
        self.win_table_view = QtGui.QTableView(self.win_tab)
        self.win_table_view.setGeometry(QtCore.QRect(0, 0, 996, 558))
        self.win_table_view.setFrameShape(QtGui.QFrame.NoFrame)
        self.win_table_view.setGridStyle(QtCore.Qt.NoPen)
        self.win_table_view.setObjectName(_fromUtf8("win_table_view"))
        self.tab_widget.addTab(self.win_tab, _fromUtf8(""))
        self.lost_tab = QtGui.QWidget()
        self.lost_tab.setObjectName(_fromUtf8("lost_tab"))
        self.lost_table_view = QtGui.QTableView(self.lost_tab)
        self.lost_table_view.setGeometry(QtCore.QRect(0, 0, 996, 558))
        self.lost_table_view.setFrameShape(QtGui.QFrame.NoFrame)
        self.lost_table_view.setGridStyle(QtCore.Qt.NoPen)
        self.lost_table_view.setObjectName(_fromUtf8("lost_table_view"))
        self.tab_widget.addTab(self.lost_tab, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Playfulbot", None))
        self.user_label.setText(_translate("MainWindow", "Usuario", None))
        self.label.setText(_translate("MainWindow", "coins", None))
        self.label_2.setText(_translate("MainWindow", "coins en juego", None))
        self.coins_p_label.setText(_translate("MainWindow", "0", None))
        self.coins_label.setText(_translate("MainWindow", "0", None))
        self.level_label.setText(_translate("MainWindow", "Nivel", None))
        self.played_label.setText(_translate("MainWindow", "Jugadas totales", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.pend_tab), _translate("MainWindow", "0 Pendientes", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.win_tab), _translate("MainWindow", "0 Ganadas", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.lost_tab), _translate("MainWindow", "0 Perdidas", None))

