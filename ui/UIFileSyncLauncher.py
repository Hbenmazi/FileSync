# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/UIFileSyncLauncher.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import boto3
from botocore.exceptions import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui.UIFileSync import UIFileSyncWidget
from PyQt5.QtCore import pyqtSignal, QObject


class UIFileSyncLauncherForm(QObject):
    connectSuccessfully = pyqtSignal(dict)

    def setupUi(self, fileSyncLauncherForm):
        fileSyncLauncherForm.setObjectName("fileSyncLauncherForm")
        fileSyncLauncherForm.resize(445, 167)
        self.form = fileSyncLauncherForm
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(fileSyncLauncherForm)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(fileSyncLauncherForm)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.endPointURLLineEdit = QtWidgets.QLineEdit(fileSyncLauncherForm)
        self.endPointURLLineEdit.setObjectName("endPointURLLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.endPointURLLineEdit)
        self.label_3 = QtWidgets.QLabel(fileSyncLauncherForm)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.secretAcessKeyLineEdit = QtWidgets.QLineEdit(fileSyncLauncherForm)
        self.secretAcessKeyLineEdit.setObjectName("secretAcessKeyLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.secretAcessKeyLineEdit)
        self.label_4 = QtWidgets.QLabel(fileSyncLauncherForm)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.bucketLineEdit = QtWidgets.QLineEdit(fileSyncLauncherForm)
        self.bucketLineEdit.setObjectName("bucketLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.bucketLineEdit)
        self.acessKeyIdLineEdit = QtWidgets.QLineEdit(fileSyncLauncherForm)
        self.acessKeyIdLineEdit.setObjectName("acessKeyIdLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.acessKeyIdLineEdit)
        self.label_2 = QtWidgets.QLabel(fileSyncLauncherForm)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.connectPushButton = QtWidgets.QPushButton(fileSyncLauncherForm)
        self.connectPushButton.setObjectName("connectPushButton")
        self.verticalLayout_2.addWidget(self.connectPushButton)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(fileSyncLauncherForm)
        QtCore.QMetaObject.connectSlotsByName(fileSyncLauncherForm)

        self.endPointURLLineEdit.setText("http://scuts3.depts.bingosoft.net:29999")
        self.acessKeyIdLineEdit.setText("8A5290742BF72419BAFF")
        self.secretAcessKeyLineEdit.setText("W0FGNTc5OTU0RkJEQjQ3RTZCQTA2MjgxOEYwRUY2RkREQ0JBMzI1NTRd")
        self.bucketLineEdit.setText("hezhiwei")
        self.setSignalSlot()

    def retranslateUi(self, fileSyncLauncherForm):
        _translate = QtCore.QCoreApplication.translate
        fileSyncLauncherForm.setWindowTitle(_translate("fileSyncLauncherForm", "Form"))
        self.label.setText(_translate("fileSyncLauncherForm", "Endpoint URL:"))
        self.label_3.setText(_translate("fileSyncLauncherForm", "Secret Access Key:"))
        self.label_4.setText(_translate("fileSyncLauncherForm", "Bucket:"))
        self.label_2.setText(_translate("fileSyncLauncherForm", "Access Key Id:"))
        self.connectPushButton.setText(_translate("fileSyncLauncherForm", "Connect"))

    def setSignalSlot(self):
        self.connectPushButton.clicked.connect(self.onConnectPushButtoClicked)
        self.connectSuccessfully.connect(self.onConnectSuccess)

    def onConnectPushButtoClicked(self):
        self.connectPushButton.setEnabled(False)
        endpoint_url = self.endPointURLLineEdit.displayText()
        aws_access_key_id = self.acessKeyIdLineEdit.displayText()
        aws_secret_access_key = self.secretAcessKeyLineEdit.displayText()
        bucket_name = self.bucketLineEdit.displayText()

        try:
            self.connectPushButton.setText('Connecting...')
            s3 = boto3.client('s3',
                              endpoint_url=endpoint_url,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)
            s3.head_bucket(Bucket=bucket_name)
        except (ValueError, ParamValidationError, EndpointConnectionError, ClientError) as e:
            if isinstance(e, ValueError) or isinstance(e, ParamValidationError):
                msg = str(e)
            else:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    msg = "Http404:Bucket {} doesn't exist.".format(bucket_name)
                elif error_code == '403':
                    msg = "Http403:Please check your access key id and secret access key."
                elif error_code == '500':
                    msg = "Http500:Internal Server Error(reached max retries: 4)."
                else:
                    msg = str(e)
            QMessageBox.information(QMessageBox(), "Fail to connent", msg, QMessageBox.Ok)

        else:
            print("连接成功")
            self.connectSuccessfully.emit({'endpoint_url': endpoint_url,
                                           'aws_access_key_id': aws_access_key_id,
                                           'aws_secret_access_key': aws_secret_access_key,
                                           'bucket_name': bucket_name
                                           })
        finally:
            self.connectPushButton.setEnabled(True)
            self.connectPushButton.setText('Connect')

    def onConnectSuccess(self, config):
        self.form.hide()
        handler_dialog = QtWidgets.QDialog()
        ui_handler = UIFileSyncWidget()
        ui_handler.config = config
        ui_handler.setupUi(handler_dialog)
        handler_dialog.show()
        handler_dialog.exec_()
