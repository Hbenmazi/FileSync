# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/UISelectDirDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import s3fs
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidgetItem

from common.utils import list_all_dir


class UISelectDirDialog(object):
    def __init__(self, parent):
        self.parent = parent

    def setupUi(self, SelectDirDialog):
        SelectDirDialog.setObjectName("SelectDirDialog")
        SelectDirDialog.resize(508, 350)
        self.dialog = SelectDirDialog
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SelectDirDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.DirListWidget = QtWidgets.QListWidget(SelectDirDialog)
        self.DirListWidget.setObjectName("DirListWidget")
        self.verticalLayout.addWidget(self.DirListWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectDirDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(SelectDirDialog)
        self.buttonBox.accepted.connect(SelectDirDialog.accept)
        self.buttonBox.rejected.connect(SelectDirDialog.reject)

        QtCore.QMetaObject.connectSlotsByName(SelectDirDialog)

        s3 = s3fs.core.S3FileSystem(key=self.parent.config.get('aws_access_key_id'),
                                    secret=self.parent.config.get('aws_secret_access_key'),
                                    client_kwargs={'endpoint_url': self.parent.config.get('endpoint_url')})
        bucket_name = self.parent.config.get('bucket_name')
        dir_list = list_all_dir(s3, bucket_name)
        self.DirListWidget.addItems(dir_list)
        self.setSignalSlot()

    def retranslateUi(self, SelectDirDialog):
        _translate = QtCore.QCoreApplication.translate
        SelectDirDialog.setWindowTitle(_translate("SelectDirDialog", "Dialog"))

    def setSignalSlot(self):
        self.buttonBox.accepted.connect(self.onAccepted)
        self.buttonBox.rejected.connect(self.onRejected)
        self.dialog.finished.connect(self.onClose)

    def onAccepted(self):
        self.parent.remote_root = self.DirListWidget.selectedItems()[0].text()
        self.parent.remoteRootLineEdit.setText(self.parent.remote_root)
        self.parent.remoteRootPushButton.setEnabled(True)

    def onRejected(self):
        self.parent.remoteRootPushButton.setEnabled(True)

    def onClose(self):
        self.parent.remoteRootPushButton.setEnabled(True)



