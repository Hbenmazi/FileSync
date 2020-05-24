# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/FileSync.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_fileSyncWidget(object):
    def setupUi(self, fileSyncWidget):
        fileSyncWidget.setObjectName("fileSyncWidget")
        fileSyncWidget.resize(459, 331)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(fileSyncWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.remoteRootPushButton = QtWidgets.QPushButton(fileSyncWidget)
        self.remoteRootPushButton.setObjectName("remoteRootPushButton")
        self.gridLayout_2.addWidget(self.remoteRootPushButton, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(fileSyncWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.remoteRootLineEdit = QtWidgets.QLineEdit(fileSyncWidget)
        self.remoteRootLineEdit.setObjectName("remoteRootLineEdit")
        self.gridLayout_2.addWidget(self.remoteRootLineEdit, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(fileSyncWidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.localRootLineEdit = QtWidgets.QLineEdit(fileSyncWidget)
        self.localRootLineEdit.setObjectName("localRootLineEdit")
        self.gridLayout_2.addWidget(self.localRootLineEdit, 0, 1, 1, 1)
        self.localRootPushButton = QtWidgets.QPushButton(fileSyncWidget)
        self.localRootPushButton.setObjectName("localRootPushButton")
        self.gridLayout_2.addWidget(self.localRootPushButton, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.startPushButton = QtWidgets.QPushButton(fileSyncWidget)
        self.startPushButton.setObjectName("startPushButton")
        self.verticalLayout.addWidget(self.startPushButton)
        self.textBrowser = QtWidgets.QTextBrowser(fileSyncWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(fileSyncWidget)
        QtCore.QMetaObject.connectSlotsByName(fileSyncWidget)

    def retranslateUi(self, fileSyncWidget):
        _translate = QtCore.QCoreApplication.translate
        fileSyncWidget.setWindowTitle(_translate("fileSyncWidget", "Form"))
        self.remoteRootPushButton.setText(_translate("fileSyncWidget", "Select"))
        self.label_2.setText(_translate("fileSyncWidget", "Remote Root:"))
        self.label.setText(_translate("fileSyncWidget", "Local Root:"))
        self.localRootPushButton.setText(_translate("fileSyncWidget", "Select"))
        self.startPushButton.setText(_translate("fileSyncWidget", "Start"))
