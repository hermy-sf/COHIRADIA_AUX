# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'COHIWizard_GUI_v4.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1163, 889)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.tab_1)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 20, 1121, 751))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_InsertHeader = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.pushButton_InsertHeader.setObjectName("pushButton_InsertHeader")
        self.gridLayout.addWidget(self.pushButton_InsertHeader, 2, 2, 1, 1)
        self.radioButton_WAVEDIT = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_WAVEDIT.sizePolicy().hasHeightForWidth())
        self.radioButton_WAVEDIT.setSizePolicy(sizePolicy)
        self.radioButton_WAVEDIT.setAutoFillBackground(True)
        self.radioButton_WAVEDIT.setObjectName("radioButton_WAVEDIT")
        self.gridLayout.addWidget(self.radioButton_WAVEDIT, 0, 2, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget_3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(14)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(10, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(11, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(12, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(13, 0, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(400)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 3, 1)
        self.tableWidget_starttime = QtWidgets.QTableWidget(self.gridLayoutWidget_3)
        self.tableWidget_starttime.setObjectName("tableWidget_starttime")
        self.tableWidget_starttime.setColumnCount(2)
        self.tableWidget_starttime.setRowCount(8)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_starttime.setItem(7, 1, item)
        self.tableWidget_starttime.horizontalHeader().setDefaultSectionSize(100)
        self.gridLayout.addWidget(self.tableWidget_starttime, 0, 1, 1, 1)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.gridLayoutWidget_3)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(1)
        self.tableWidget_3.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_3.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_3.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_3.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_3.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(3, 0, item)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(600)
        self.tableWidget_3.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget_3.verticalHeader().setDefaultSectionSize(37)
        self.gridLayout.addWidget(self.tableWidget_3, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_8.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(251, 255, 203))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(251, 255, 203))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 254, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        self.label_8.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAutoFillBackground(True)
        self.label_8.setStyleSheet("rgb(255, 254, 210)")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tab_3)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(9, 10, 1111, 741))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_4.addWidget(self.lineEdit_2, 0, 0, 1, 1)
        self.spinBoxminSNR_ScannerTab = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxminSNR_ScannerTab.setMinimum(0)
        self.spinBoxminSNR_ScannerTab.setMaximum(100)
        self.spinBoxminSNR_ScannerTab.setSingleStep(5)
        self.spinBoxminSNR_ScannerTab.setProperty("value", 10)
        self.spinBoxminSNR_ScannerTab.setObjectName("spinBoxminSNR_ScannerTab")
        self.gridLayout_4.addWidget(self.spinBoxminSNR_ScannerTab, 0, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 2, 2, 1, 1)
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.gridLayoutWidget_2)
        self.horizontalScrollBar.setMaximum(1000)
        self.horizontalScrollBar.setPageStep(1)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.gridLayout_4.addWidget(self.horizontalScrollBar, 5, 0, 1, 4)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 2, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.gridLayoutWidget_2)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_4.addWidget(self.graphicsView, 4, 0, 1, 4)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 1, 2, 1, 1)
        self.spinBoxminBaselineoffset = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxminBaselineoffset.setMinimum(-20)
        self.spinBoxminBaselineoffset.setMaximum(20)
        self.spinBoxminBaselineoffset.setSingleStep(5)
        self.spinBoxminBaselineoffset.setProperty("value", 5)
        self.spinBoxminBaselineoffset.setObjectName("spinBoxminBaselineoffset")
        self.gridLayout_4.addWidget(self.spinBoxminBaselineoffset, 1, 3, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_4)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1121, 771))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.progressBar_2 = QtWidgets.QProgressBar(self.gridLayoutWidget)
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName("progressBar_2")
        self.gridLayout_3.addWidget(self.progressBar_2, 10, 0, 1, 8)
        self.pushButton_Scan = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_Scan.setObjectName("pushButton_Scan")
        self.gridLayout_3.addWidget(self.pushButton_Scan, 3, 5, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 9, 0, 1, 8)
        self.pushButtonDiscard = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonDiscard.setObjectName("pushButtonDiscard")
        self.gridLayout_3.addWidget(self.pushButtonDiscard, 3, 7, 1, 1)
        self.Annotate_listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.Annotate_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Annotate_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Annotate_listWidget.setAlternatingRowColors(True)
        self.Annotate_listWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.Annotate_listWidget.setMovement(QtWidgets.QListView.Free)
        self.Annotate_listWidget.setObjectName("Annotate_listWidget")
        item = QtWidgets.QListWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 127))
        brush.setStyle(QtCore.Qt.Dense3Pattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 50))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.Annotate_listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.Annotate_listWidget.addItem(item)
        self.gridLayout_3.addWidget(self.Annotate_listWidget, 8, 0, 1, 8)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 3, 3, 1, 1)
        self.spinBoxNumScan = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxNumScan.setProperty("value", 20)
        self.spinBoxNumScan.setObjectName("spinBoxNumScan")
        self.gridLayout_3.addWidget(self.spinBoxNumScan, 3, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 3, 1, 1, 1)
        self.pushButtonAnnotate = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonAnnotate.setObjectName("pushButtonAnnotate")
        self.gridLayout_3.addWidget(self.pushButtonAnnotate, 3, 6, 1, 1)
        self.spinBoxminSNR = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxminSNR.setMinimum(0)
        self.spinBoxminSNR.setMaximum(100)
        self.spinBoxminSNR.setSingleStep(5)
        self.spinBoxminSNR.setProperty("value", 10)
        self.spinBoxminSNR.setObjectName("spinBoxminSNR")
        self.gridLayout_3.addWidget(self.spinBoxminSNR, 3, 2, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 4, 0, 1, 8)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        #self.menubar = File(MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1163, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFile_open = QtWidgets.QAction(MainWindow)
        self.actionFile_open.setCheckable(False)
        self.actionFile_open.setEnabled(True)
        self.actionFile_open.setObjectName("actionFile_open")
        self.actionSave_header_to_template = QtWidgets.QAction(MainWindow)
        self.actionSave_header_to_template.setObjectName("actionSave_header_to_template")
        self.actionOverwrite_header = QtWidgets.QAction(MainWindow)
        self.actionOverwrite_header.setObjectName("actionOverwrite_header")
        self.actionLoad_template_header = QtWidgets.QAction(MainWindow)
        self.actionLoad_template_header.setObjectName("actionLoad_template_header")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionFile_open)
        self.menuFile.addAction(self.actionOverwrite_header)
        self.menuFile.addAction(self.actionSave_header_to_template)
        self.menuFile.addAction(self.actionLoad_template_header)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setToolTip(_translate("MainWindow", "generate annotation basis by comparing MWLIST, display candidates at next frequency"))
        self.tabWidget.setToolTip(_translate("MainWindow", "<html><head/><body><p>Chose the wanted toolkit</p></body></html>"))
        self.pushButton_InsertHeader.setText(_translate("MainWindow", "Insert Header"))
        self.radioButton_WAVEDIT.setToolTip(_translate("MainWindow", "make this table editable by clicking \'edit\'"))
        self.radioButton_WAVEDIT.setText(_translate("MainWindow", "EDIT"))
        self.tableWidget.setToolTip(_translate("MainWindow", "make this table editable by clicking \'edit\'"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Filesize"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "sdr_nChunksize"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "wFormatTag"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "nChannels"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Sample rate"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "bytes per second"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "nBlockalign"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "bits per sample"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "centerfreq"))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "dataChunksize"))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "ADFrequency"))
        item = self.tableWidget.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "IFFrequency"))
        item = self.tableWidget.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "Bandwidth"))
        item = self.tableWidget.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "IQOffset"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "value"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("MainWindow", "2"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(5, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(6, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(7, 0)
        item.setText(_translate("MainWindow", "16"))
        item = self.tableWidget.item(8, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(9, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(10, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(11, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(12, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.item(13, 0)
        item.setText(_translate("MainWindow", "0"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tableWidget_starttime.setToolTip(_translate("MainWindow", "make this table editable by clicking \'edit\'"))
        item = self.tableWidget_starttime.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "YYYY"))
        item = self.tableWidget_starttime.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "MM"))
        item = self.tableWidget_starttime.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "---"))
        item = self.tableWidget_starttime.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "DD"))
        item = self.tableWidget_starttime.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "HH"))
        item = self.tableWidget_starttime.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "mm"))
        item = self.tableWidget_starttime.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "ss"))
        item = self.tableWidget_starttime.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "ms"))
        item = self.tableWidget_starttime.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Start"))
        item = self.tableWidget_starttime.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Stop"))
        __sortingEnabled = self.tableWidget_starttime.isSortingEnabled()
        self.tableWidget_starttime.setSortingEnabled(False)
        item = self.tableWidget_starttime.item(0, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(0, 1)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(1, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(1, 1)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(2, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(2, 1)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(3, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(3, 1)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(4, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(4, 1)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(5, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(5, 1)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(6, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(6, 1)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(7, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_starttime.item(7, 1)
        item.setText(_translate("MainWindow", "0"))
        self.tableWidget_starttime.setSortingEnabled(__sortingEnabled)
        self.tableWidget_3.setToolTip(_translate("MainWindow", "make this table editable by clicking \'edit\'"))
        item = self.tableWidget_3.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "nextfilename"))
        item = self.tableWidget_3.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "SDR Type"))
        item = self.tableWidget_3.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Start"))
        item = self.tableWidget_3.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "dataheader"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "value"))
        __sortingEnabled = self.tableWidget_3.isSortingEnabled()
        self.tableWidget_3.setSortingEnabled(False)
        item = self.tableWidget_3.item(0, 0)
        item.setText(_translate("MainWindow", "-"))
        item = self.tableWidget_3.item(1, 0)
        item.setText(_translate("MainWindow", "-"))
        item = self.tableWidget_3.item(2, 0)
        item.setText(_translate("MainWindow", "-"))
        item = self.tableWidget_3.item(3, 0)
        item.setText(_translate("MainWindow", "-"))
        self.tableWidget_3.setSortingEnabled(__sortingEnabled)
        self.label_8.setText(_translate("MainWindow", "Convert dat -> wav by inserting current wav header"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "WAV Header"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Resampler"))
        self.lineEdit_2.setText(_translate("MainWindow", "Display the spectrum at different times of the record by dragging the scrollbar"))
        self.spinBoxminSNR_ScannerTab.setToolTip(_translate("MainWindow", "select number of steps for scanning through the spectrum and averaging SNRs"))
        self.label_5.setText(_translate("MainWindow", " "))
        self.horizontalScrollBar.setToolTip(_translate("MainWindow", "move slider to browse through the record and plot spectra "))
        self.label_4.setToolTip(_translate("MainWindow", "minimum SNR for auto-selection of peaks"))
        self.label_4.setText(_translate("MainWindow", "min SNR"))
        self.graphicsView.setToolTip(_translate("MainWindow", "space for spectrum plot"))
        self.label_7.setToolTip(_translate("MainWindow", "baseline offset from automated baseline"))
        self.label_7.setText(_translate("MainWindow", "baseline offset"))
        self.spinBoxminBaselineoffset.setToolTip(_translate("MainWindow", "select baseline offset from automated baseline"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Scanner"))
        self.pushButton_Scan.setToolTip(_translate("MainWindow", "Scan record, extract peaks with SNR > min SNR"))
        self.pushButton_Scan.setText(_translate("MainWindow", "Scan"))
        self.label.setText(_translate("MainWindow", "Status:"))
        self.pushButtonDiscard.setToolTip(_translate("MainWindow", "ignore current table and proceed to next frequency"))
        self.pushButtonDiscard.setText(_translate("MainWindow", "Discard"))
        self.Annotate_listWidget.setToolTip(_translate("MainWindow", "space for stations list"))
        __sortingEnabled = self.Annotate_listWidget.isSortingEnabled()
        self.Annotate_listWidget.setSortingEnabled(False)
        item = self.Annotate_listWidget.item(0)
        item.setText(_translate("MainWindow", "TESTITEM1"))
        item = self.Annotate_listWidget.item(1)
        item.setText(_translate("MainWindow", "TESTITEM2"))
        self.Annotate_listWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setToolTip(_translate("MainWindow", "number of evaluation steps when scanning record for peaks"))
        self.label_2.setText(_translate("MainWindow", "#scan steps"))
        self.spinBoxNumScan.setToolTip(_translate("MainWindow", "select number of steps for scanning through the spectrum and averaging SNRs"))
        self.label_3.setToolTip(_translate("MainWindow", "minimum SNR for auto-selection of peaks"))
        self.label_3.setText(_translate("MainWindow", "min SNR (dB)"))
        self.pushButtonAnnotate.setToolTip(_translate("MainWindow", "assign peaks to candidates of stations"))
        self.pushButtonAnnotate.setText(_translate("MainWindow", "Annotate"))
        self.spinBoxminSNR.setToolTip(_translate("MainWindow", "select number of steps for scanning through the spectrum and averaging SNRs"))
        self.lineEdit.setText(_translate("MainWindow", "Frequency:"))
        self.label_6.setToolTip(_translate("MainWindow", "baseline offset , adjustable in Tan \'Scanner\'"))
        self.label_6.setText(_translate("MainWindow", "Baseline Offset: "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Annotate"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionFile_open.setText(_translate("MainWindow", "File open"))
        self.actionSave_header_to_template.setText(_translate("MainWindow", "Save header to template"))
        self.actionOverwrite_header.setText(_translate("MainWindow", "Overwrite header"))
        self.actionLoad_template_header.setText(_translate("MainWindow", "Load template header"))
#from file import File


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
