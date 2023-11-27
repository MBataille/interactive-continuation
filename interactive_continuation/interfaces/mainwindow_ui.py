# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

from .mplwidget import MplWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        self.actionSave_branch = QAction(MainWindow)
        self.actionSave_branch.setObjectName(u"actionSave_branch")
        self.actionLoad_branch = QAction(MainWindow)
        self.actionLoad_branch.setObjectName(u"actionLoad_branch")
        self.actionNew_branch = QAction(MainWindow)
        self.actionNew_branch.setObjectName(u"actionNew_branch")
        self.actionSplit_branches = QAction(MainWindow)
        self.actionSplit_branches.setObjectName(u"actionSplit_branches")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionDelete_branch = QAction(MainWindow)
        self.actionDelete_branch.setObjectName(u"actionDelete_branch")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.contparamsframe = QFrame(self.centralwidget)
        self.contparamsframe.setObjectName(u"contparamsframe")
        self.contparamsframe.setMinimumSize(QSize(400, 100))
        self.contparamsframe.setMaximumSize(QSize(16777215, 150))
        self.contparamsframe.setFrameShape(QFrame.StyledPanel)
        self.contparamsframe.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.contparamsframe)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.leftverticalLayout = QVBoxLayout()
        self.leftverticalLayout.setObjectName(u"leftverticalLayout")
        self.equationsHLayout = QHBoxLayout()
        self.equationsHLayout.setObjectName(u"equationsHLayout")
        self.eqn_label = QLabel(self.contparamsframe)
        self.eqn_label.setObjectName(u"eqn_label")
        self.eqn_label.setMinimumSize(QSize(50, 0))
        self.eqn_label.setAlignment(Qt.AlignCenter)

        self.equationsHLayout.addWidget(self.eqn_label)

        self.eqn_combobox = QComboBox(self.contparamsframe)
        self.eqn_combobox.addItem("")
        self.eqn_combobox.addItem("")
        self.eqn_combobox.setObjectName(u"eqn_combobox")
        self.eqn_combobox.setMinimumSize(QSize(50, 0))

        self.equationsHLayout.addWidget(self.eqn_combobox)

        self.initcond_label = QLabel(self.contparamsframe)
        self.initcond_label.setObjectName(u"initcond_label")

        self.equationsHLayout.addWidget(self.initcond_label)

        self.initcond_entry = QLineEdit(self.contparamsframe)
        self.initcond_entry.setObjectName(u"initcond_entry")
        self.initcond_entry.setMinimumSize(QSize(100, 0))

        self.equationsHLayout.addWidget(self.initcond_entry)

        self.initcond_pushButton = QPushButton(self.contparamsframe)
        self.initcond_pushButton.setObjectName(u"initcond_pushButton")

        self.equationsHLayout.addWidget(self.initcond_pushButton)


        self.leftverticalLayout.addLayout(self.equationsHLayout)

        self.contparamsHLayout = QHBoxLayout()
        self.contparamsHLayout.setObjectName(u"contparamsHLayout")
        self.ds_label = QLabel(self.contparamsframe)
        self.ds_label.setObjectName(u"ds_label")
        self.ds_label.setMinimumSize(QSize(30, 0))

        self.contparamsHLayout.addWidget(self.ds_label)

        self.ds_entry = QLineEdit(self.contparamsframe)
        self.ds_entry.setObjectName(u"ds_entry")

        self.contparamsHLayout.addWidget(self.ds_entry)

        self.atol_label = QLabel(self.contparamsframe)
        self.atol_label.setObjectName(u"atol_label")
        self.atol_label.setMinimumSize(QSize(30, 0))

        self.contparamsHLayout.addWidget(self.atol_label)

        self.atol_entry = QLineEdit(self.contparamsframe)
        self.atol_entry.setObjectName(u"atol_entry")

        self.contparamsHLayout.addWidget(self.atol_entry)

        self.w_x_label = QLabel(self.contparamsframe)
        self.w_x_label.setObjectName(u"w_x_label")
        self.w_x_label.setMinimumSize(QSize(30, 0))

        self.contparamsHLayout.addWidget(self.w_x_label)

        self.w_x_entry = QLineEdit(self.contparamsframe)
        self.w_x_entry.setObjectName(u"w_x_entry")

        self.contparamsHLayout.addWidget(self.w_x_entry)

        self.direction_label = QLabel(self.contparamsframe)
        self.direction_label.setObjectName(u"direction_label")

        self.contparamsHLayout.addWidget(self.direction_label)

        self.direction_combobox = QComboBox(self.contparamsframe)
        self.direction_combobox.addItem("")
        self.direction_combobox.addItem("")
        self.direction_combobox.setObjectName(u"direction_combobox")

        self.contparamsHLayout.addWidget(self.direction_combobox)


        self.leftverticalLayout.addLayout(self.contparamsHLayout)

        self.branchHLayout = QHBoxLayout()
        self.branchHLayout.setObjectName(u"branchHLayout")
        self.xaxis_label = QLabel(self.contparamsframe)
        self.xaxis_label.setObjectName(u"xaxis_label")
        self.xaxis_label.setAlignment(Qt.AlignCenter)

        self.branchHLayout.addWidget(self.xaxis_label)

        self.xaxis_combobox = QComboBox(self.contparamsframe)
        self.xaxis_combobox.setObjectName(u"xaxis_combobox")

        self.branchHLayout.addWidget(self.xaxis_combobox)

        self.yaxis_label = QLabel(self.contparamsframe)
        self.yaxis_label.setObjectName(u"yaxis_label")
        self.yaxis_label.setAlignment(Qt.AlignCenter)

        self.branchHLayout.addWidget(self.yaxis_label)

        self.yaxis_combobox = QComboBox(self.contparamsframe)
        self.yaxis_combobox.setObjectName(u"yaxis_combobox")

        self.branchHLayout.addWidget(self.yaxis_combobox)

        self.saveprofile_checkbox = QCheckBox(self.contparamsframe)
        self.saveprofile_checkbox.setObjectName(u"saveprofile_checkbox")
        self.saveprofile_checkbox.setChecked(True)

        self.branchHLayout.addWidget(self.saveprofile_checkbox)

        self.save_branch_pushButton = QPushButton(self.contparamsframe)
        self.save_branch_pushButton.setObjectName(u"save_branch_pushButton")

        self.branchHLayout.addWidget(self.save_branch_pushButton)


        self.leftverticalLayout.addLayout(self.branchHLayout)


        self.horizontalLayout_11.addLayout(self.leftverticalLayout)

        self.rightverticalLayout = QVBoxLayout()
        self.rightverticalLayout.setObjectName(u"rightverticalLayout")
        self.initcondHLayout = QHBoxLayout()
        self.initcondHLayout.setObjectName(u"initcondHLayout")
        self.branch_label = QLabel(self.contparamsframe)
        self.branch_label.setObjectName(u"branch_label")

        self.initcondHLayout.addWidget(self.branch_label)

        self.branch_entry = QLineEdit(self.contparamsframe)
        self.branch_entry.setObjectName(u"branch_entry")

        self.initcondHLayout.addWidget(self.branch_entry)


        self.rightverticalLayout.addLayout(self.initcondHLayout)

        self.contsettingsHLayout = QHBoxLayout()
        self.contsettingsHLayout.setObjectName(u"contsettingsHLayout")
        self.playpause_pushButton = QPushButton(self.contparamsframe)
        self.playpause_pushButton.setObjectName(u"playpause_pushButton")

        self.contsettingsHLayout.addWidget(self.playpause_pushButton)


        self.rightverticalLayout.addLayout(self.contsettingsHLayout)

        self.timeHLayout = QHBoxLayout()
        self.timeHLayout.setObjectName(u"timeHLayout")
        self.elapsedtime_label = QLabel(self.contparamsframe)
        self.elapsedtime_label.setObjectName(u"elapsedtime_label")

        self.timeHLayout.addWidget(self.elapsedtime_label)

        self.avgtime_label = QLabel(self.contparamsframe)
        self.avgtime_label.setObjectName(u"avgtime_label")

        self.timeHLayout.addWidget(self.avgtime_label)


        self.rightverticalLayout.addLayout(self.timeHLayout)


        self.horizontalLayout_11.addLayout(self.rightverticalLayout)


        self.verticalLayout_3.addWidget(self.contparamsframe)

        self.mainplotframe = QFrame(self.centralwidget)
        self.mainplotframe.setObjectName(u"mainplotframe")
        self.mainplotframe.setMinimumSize(QSize(400, 400))
        self.mainplotframe.setFrameShape(QFrame.StyledPanel)
        self.mainplotframe.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.mainplotframe)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mainplot = MplWidget(self.mainplotframe)
        self.mainplot.setObjectName(u"mainplot")
        self.mainplot.setMinimumSize(QSize(400, 400))

        self.horizontalLayout.addWidget(self.mainplot)


        self.verticalLayout_3.addWidget(self.mainplotframe)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.eqnparams_frame = QFrame(self.centralwidget)
        self.eqnparams_frame.setObjectName(u"eqnparams_frame")
        self.eqnparams_frame.setMinimumSize(QSize(200, 100))
        self.eqnparams_frame.setFrameShape(QFrame.StyledPanel)
        self.eqnparams_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.eqnparams_frame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_11 = QLabel(self.eqnparams_frame)
        self.label_11.setObjectName(u"label_11")
        font = QFont()
        font.setPointSize(14)
        self.label_11.setFont(font)

        self.verticalLayout_8.addWidget(self.label_11)

        self.params_HLayout = QHBoxLayout()
        self.params_HLayout.setObjectName(u"params_HLayout")
        self.param1_label = QLabel(self.eqnparams_frame)
        self.param1_label.setObjectName(u"param1_label")

        self.params_HLayout.addWidget(self.param1_label)

        self.param1_entry = QLineEdit(self.eqnparams_frame)
        self.param1_entry.setObjectName(u"param1_entry")

        self.params_HLayout.addWidget(self.param1_entry)

        self.param2_label = QLabel(self.eqnparams_frame)
        self.param2_label.setObjectName(u"param2_label")

        self.params_HLayout.addWidget(self.param2_label)

        self.param2_entry = QLineEdit(self.eqnparams_frame)
        self.param2_entry.setObjectName(u"param2_entry")

        self.params_HLayout.addWidget(self.param2_entry)


        self.verticalLayout_8.addLayout(self.params_HLayout)


        self.verticalLayout_2.addWidget(self.eqnparams_frame)

        self.contlog_frame = QFrame(self.centralwidget)
        self.contlog_frame.setObjectName(u"contlog_frame")
        self.contlog_frame.setMinimumSize(QSize(200, 100))
        self.contlog_frame.setFrameShape(QFrame.StyledPanel)
        self.contlog_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.contlog_frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.contlogtitle_label = QLabel(self.contlog_frame)
        self.contlogtitle_label.setObjectName(u"contlogtitle_label")
        font1 = QFont()
        font1.setFamilies([u"Open Sans"])
        font1.setPointSize(14)
        self.contlogtitle_label.setFont(font1)

        self.verticalLayout_6.addWidget(self.contlogtitle_label)

        self.log_label = QLabel(self.contlog_frame)
        self.log_label.setObjectName(u"log_label")

        self.verticalLayout_6.addWidget(self.log_label)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)


        self.verticalLayout_2.addWidget(self.contlog_frame)

        self.secondaryplot_frame = QFrame(self.centralwidget)
        self.secondaryplot_frame.setObjectName(u"secondaryplot_frame")
        self.secondaryplot_frame.setMinimumSize(QSize(200, 400))
        self.secondaryplot_frame.setFrameShape(QFrame.StyledPanel)
        self.secondaryplot_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.secondaryplot_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.secondaryplot = MplWidget(self.secondaryplot_frame)
        self.secondaryplot.setObjectName(u"secondaryplot")
        self.secondaryplot.setMinimumSize(QSize(100, 200))

        self.verticalLayout.addWidget(self.secondaryplot)


        self.verticalLayout_2.addWidget(self.secondaryplot_frame)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuFile_2 = QMenu(self.menubar)
        self.menuFile_2.setObjectName(u"menuFile_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile_2.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuFile.addAction(self.actionNew_branch)
        self.menuFile.addAction(self.actionLoad_branch)
        self.menuFile.addAction(self.actionSave_branch)
        self.menuFile.addAction(self.actionDelete_branch)
        self.menuFile.addAction(self.actionSplit_branches)
        self.menuSettings.addAction(self.actionSettings)
        self.menuFile_2.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave_branch.setText(QCoreApplication.translate("MainWindow", u"Save branch", None))
        self.actionLoad_branch.setText(QCoreApplication.translate("MainWindow", u"Load branch", None))
        self.actionNew_branch.setText(QCoreApplication.translate("MainWindow", u"New branch", None))
        self.actionSplit_branches.setText(QCoreApplication.translate("MainWindow", u"Split branches", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionDelete_branch.setText(QCoreApplication.translate("MainWindow", u"Delete branch", None))
        self.eqn_label.setText(QCoreApplication.translate("MainWindow", u"Equation", None))
        self.eqn_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"test1", None))
        self.eqn_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"test2", None))

        self.initcond_label.setText(QCoreApplication.translate("MainWindow", u"Initial condition", None))
        self.initcond_pushButton.setText(QCoreApplication.translate("MainWindow", u"load", None))
        self.ds_label.setText(QCoreApplication.translate("MainWindow", u"ds", None))
        self.atol_label.setText(QCoreApplication.translate("MainWindow", u"atol", None))
        self.w_x_label.setText(QCoreApplication.translate("MainWindow", u"w_x", None))
        self.direction_label.setText(QCoreApplication.translate("MainWindow", u"direction", None))
        self.direction_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"forward", None))
        self.direction_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"backward", None))

        self.xaxis_label.setText(QCoreApplication.translate("MainWindow", u"x axis", None))
        self.yaxis_label.setText(QCoreApplication.translate("MainWindow", u"y axis", None))
        self.saveprofile_checkbox.setText(QCoreApplication.translate("MainWindow", u"save profile", None))
        self.save_branch_pushButton.setText(QCoreApplication.translate("MainWindow", u"save branch data", None))
        self.branch_label.setText(QCoreApplication.translate("MainWindow", u"Branch name", None))
        self.playpause_pushButton.setText(QCoreApplication.translate("MainWindow", u"play / pause", None))
        self.elapsedtime_label.setText(QCoreApplication.translate("MainWindow", u"Elapsed time: 0 s", None))
        self.avgtime_label.setText(QCoreApplication.translate("MainWindow", u"Avg time per point: 0s", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Equation Parameters", None))
        self.param1_label.setText(QCoreApplication.translate("MainWindow", u"theta", None))
        self.param2_label.setText(QCoreApplication.translate("MainWindow", u"epsilon", None))
        self.contlogtitle_label.setText(QCoreApplication.translate("MainWindow", u"Contination Log", None))
        self.log_label.setText(QCoreApplication.translate("MainWindow", u"Step 0. No Continuation", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Branch", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuFile_2.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

