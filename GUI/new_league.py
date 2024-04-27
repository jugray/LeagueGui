import sys
from PyQt5 import uic, QtWidgets, QtGui


Ui_League_Manager_Main, QtBaseWindow = uic.loadUiType("new_league.ui")

class NewLeagueDialog(QtBaseWindow, Ui_League_Manager_Main):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setStyleSheet("background-color: lightsteelblue;")
        self.setWindowIcon(QtGui.QIcon('img/stone.png'))
        self.setStyleSheet("""
        background-image: url('img/stone.png');
        background-repeat: no-repeat;
        background-position: center;
        background-color: lightsteelblue;
        """)

    def get_league_name(self):
        return self.new_league_line.text()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = NewLeagueDialog()
    window.show()
    sys.exit(app.exec_())