import sys
from PyQt5 import QtWidgets
from ui.UIFileSyncLauncher import UIFileSyncLauncherForm

app = QtWidgets.QApplication(sys.argv)
launcher_widget = QtWidgets.QWidget()
ui_launcher = UIFileSyncLauncherForm()
ui_launcher.setupUi(launcher_widget)
launcher_widget.show()
sys.exit(app.exec_())
