# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QToolBar, QWidget)

from myview import MyPdfView
import semsearch_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1302, 1179)
        self.actionOpen_PDF = QAction(MainWindow)
        self.actionOpen_PDF.setObjectName(u"actionOpen_PDF")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionOpen_PDF_Tbar = QAction(MainWindow)
        self.actionOpen_PDF_Tbar.setObjectName(u"actionOpen_PDF_Tbar")
        icon = QIcon()
        icon.addFile(u":/icons/icons/document-pdf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionOpen_PDF_Tbar.setIcon(icon)
        self.actionOpen_PDF_Tbar.setMenuRole(QAction.NoRole)
        self.actionClose_App_Tbar = QAction(MainWindow)
        self.actionClose_App_Tbar.setObjectName(u"actionClose_App_Tbar")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/cross.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionClose_App_Tbar.setIcon(icon1)
        self.actionClose_App_Tbar.setMenuRole(QAction.NoRole)
        self.actionOpen_Recent = QAction(MainWindow)
        self.actionOpen_Recent.setObjectName(u"actionOpen_Recent")
        self.actionfiles = QAction(MainWindow)
        self.actionfiles.setObjectName(u"actionfiles")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblResults = QLabel(self.centralwidget)
        self.lblResults.setObjectName(u"lblResults")

        self.gridLayout.addWidget(self.lblResults, 0, 0, 1, 1)

        self.lblQuery = QLabel(self.centralwidget)
        self.lblQuery.setObjectName(u"lblQuery")

        self.gridLayout.addWidget(self.lblQuery, 0, 1, 1, 1)

        self.editQuery = QLineEdit(self.centralwidget)
        self.editQuery.setObjectName(u"editQuery")
        self.editQuery.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.editQuery, 0, 2, 1, 1)

        self.btnSearch = QPushButton(self.centralwidget)
        self.btnSearch.setObjectName(u"btnSearch")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/magnifier-left-btn.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnSearch.setIcon(icon2)

        self.gridLayout.addWidget(self.btnSearch, 0, 3, 1, 1)

        self.tblResults = QTableWidget(self.centralwidget)
        self.tblResults.setObjectName(u"tblResults")
        self.tblResults.setMaximumSize(QSize(375, 16777215))

        self.gridLayout.addWidget(self.tblResults, 1, 0, 1, 1)

        self.pdfView = MyPdfView(self.centralwidget)
        self.pdfView.setObjectName(u"pdfView")

        self.gridLayout.addWidget(self.pdfView, 1, 1, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1302, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuOpen_Recent = QMenu(self.menuFile)
        self.menuOpen_Recent.setObjectName(u"menuOpen_Recent")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen_PDF)
        self.menuFile.addAction(self.menuOpen_Recent.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.toolBar.addAction(self.actionOpen_PDF_Tbar)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClose_App_Tbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_PDF.setText(QCoreApplication.translate("MainWindow", u"&Open PDF...", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"&Close", None))
        self.actionOpen_PDF_Tbar.setText(QCoreApplication.translate("MainWindow", u"Open PDF", None))
        self.actionOpen_PDF_Tbar.setIconText(QCoreApplication.translate("MainWindow", u"Open PDF", None))
#if QT_CONFIG(tooltip)
        self.actionOpen_PDF_Tbar.setToolTip(QCoreApplication.translate("MainWindow", u"Open PDF file", None))
#endif // QT_CONFIG(tooltip)
        self.actionClose_App_Tbar.setText(QCoreApplication.translate("MainWindow", u"Close application", None))
        self.actionClose_App_Tbar.setIconText(QCoreApplication.translate("MainWindow", u"Close application", None))
#if QT_CONFIG(tooltip)
        self.actionClose_App_Tbar.setToolTip(QCoreApplication.translate("MainWindow", u"Close application", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpen_Recent.setText(QCoreApplication.translate("MainWindow", u"Open Recent", None))
        self.actionfiles.setText(QCoreApplication.translate("MainWindow", u"[none]", None))
        self.lblResults.setText(QCoreApplication.translate("MainWindow", u"Query Results", None))
        self.lblQuery.setText(QCoreApplication.translate("MainWindow", u"Query:", None))
        self.btnSearch.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuOpen_Recent.setTitle(QCoreApplication.translate("MainWindow", u"Open &Recent", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

