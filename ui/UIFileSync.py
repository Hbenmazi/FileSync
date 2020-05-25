# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/UIFileSync.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import os
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEventLoop
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QListWidget, QListWidgetItem, QApplication, QMessageBox, QDialog
import s3fs

from FileSyncLauncher import FileSyncLauncher
from common.StdOutRedirect import StdOutRedirect
from ui.UISelectDirDialog import UISelectDirDialog
import threading


class UIFileSyncWidget(object):
    config = {}
    local_root = None
    remote_root = None
    launcher_thread = None
    _stdout = StdOutRedirect()

    def setupUi(self, fileSyncWidget):
        fileSyncWidget.setObjectName("fileSyncWidget")
        fileSyncWidget.resize(600, 331)
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
        # self.widget.closed.connect(self.close)
        self.widget.closeEvent = self.closeEvent
        self._stdout.printOccur.connect(lambda x: self._append_text(x))

    def start(self):
        if self.startPushButton.text() == 'Start':
            self.localRootPushButton.setEnabled(False)
            self.remoteRootPushButton.setEnabled(False)
            self._stdout.start()
            self.startPushButton.setText('Running..')
            self.startPushButton.setEnabled(False)
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
            pass

    def closeEvent(self, event):
        print("Terminating........")
        if self.launcher_thread and self.launcher_thread.is_alive():
            self.launcher_thread.terminate()

            # def wait(launcher_thread):
            #     while launcher_thread.is_alive():
            #         pass
            #
            # wait_thread = threading.Thread(target=wait, args=(self.launcher_thread,))
            # wait_thread.start()
            # # wait_thread.join()
        else:
            pass

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

    def _append_text(self, msg):
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)
        self.textBrowser.insertPlainText(msg)
        # refresh textedit show, refer) https://doc.qt.io/qt-5/qeventloop.html#ProcessEventsFlag-enum
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
