# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/UIFileSync.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QListWidget, QListWidgetItem
import s3fs

from FileSyncLauncher import FileSyncLauncher
from ui.UISelectDirDialog import UISelectDirDialog


class UIFileSyncWidget(object):
    config = {}
    local_root = None
    remote_root = None
    launcher_thread = None

    def setupUi(self, fileSyncWidget):
        fileSyncWidget.setObjectName("fileSyncWidget")
        fileSyncWidget.resize(459, 331)
        self.widget = fileSyncWidget
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

        self.localRootLineEdit.setReadOnly(True)
        self.remoteRootLineEdit.setReadOnly(True)
        self.setSignalSlot()

    def retranslateUi(self, fileSyncWidget):
        _translate = QtCore.QCoreApplication.translate
        fileSyncWidget.setWindowTitle(_translate("fileSyncWidget", "Form"))
        self.remoteRootPushButton.setText(_translate("fileSyncWidget", "Select"))
        self.label_2.setText(_translate("fileSyncWidget", "Remote Root:"))
        self.label.setText(_translate("fileSyncWidget", "Local Root:"))
        self.localRootPushButton.setText(_translate("fileSyncWidget", "Select"))
        self.startPushButton.setText(_translate("fileSyncWidget", "Start"))

    def setSignalSlot(self):
        # Todo
        self.localRootPushButton.clicked.connect(self.selectLocalDir)
        self.remoteRootPushButton.clicked.connect(self.selectRootDir)
        self.startPushButton.clicked.connect(self.start)

    def start(self):
        if self.startPushButton.text() == 'Start':
            self.localRootPushButton.setEnabled(False)
            self.remoteRootPushButton.setEnabled(False)
            self.startPushButton.setText('Pause')
            endpoint_url = self.config.get('endpoint_url')
            aws_access_key_id = self.config.get('aws_access_key_id')
            aws_secret_access_key = self.config.get('aws_secret_access_key')
            bucket_name = self.config.get('bucket_name')
            remote_root = self.remote_root.strip(bucket_name + '/')
            local_root = self.local_root

            self.launcher_thread = FileSyncLauncher(endpoint_url,
                                                    aws_access_key_id,
                                                    aws_secret_access_key,
                                                    local_root=local_root,
                                                    remote_root=remote_root,
                                                    bucket_name=bucket_name)
            self.launcher_thread.start()
        else:
            self.localRootPushButton.setEnabled(True)
            self.remoteRootPushButton.setEnabled(True)
            self.startPushButton.setText('Start')

            if self.launcher_thread:
                self.launcher_thread.stop = True

    def selectLocalDir(self):
        self.localRootPushButton.setEnabled(False)
        self.local_root = str(QFileDialog.getExistingDirectory(self.widget, "Select Local Root"))
        self.localRootLineEdit.setText(self.local_root)
        self.localRootPushButton.setEnabled(True)

    def selectRootDir(self):
        self.remoteRootPushButton.setEnabled(False)
        select_dir_dialog = QtWidgets.QDialog()
        ui_select_dir_dialog = UISelectDirDialog(self)
        ui_select_dir_dialog.setupUi(select_dir_dialog)
        select_dir_dialog.show()
        select_dir_dialog.exec_()
