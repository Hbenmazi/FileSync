import sys
from PyQt5 import QtWidgets
from ui.UIFileSyncLauncher import UIFileSyncLauncherForm
from ui.UIFileSync import UIFileSyncWidget

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher_widget = QtWidgets.QWidget()
    ui_launcher = UIFileSyncLauncherForm()
    ui_launcher.setupUi(launcher_widget)
    launcher_widget.show()

    sys.exit(app.exec_())

    # endpoint_url = "http://scuts3.depts.bingosoft.net:29999"
    # aws_access_key_id = "8A5290742BF72419BAFF"
    # aws_secret_access_key = "W0FGNTc5OTU0RkJEQjQ3RTZCQTA2MjgxOEYwRUY2RkREQ0JBMzI1NTRd"
    # remote_root = 'remote'
    # local_root = 'local'
    #
    # launcher = FileSyncLauncher(endpoint_url,
    #                             aws_access_key_id,
    #                             aws_secret_access_key,
    #                             local_root=local_root,
    #                             remote_root=remote_root)
    # launcher.run()
