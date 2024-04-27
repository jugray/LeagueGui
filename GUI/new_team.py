import sys
from PyQt5 import uic, QtWidgets, QtGui


Ui_League_Manager_Main, QtBaseWindow = uic.loadUiType("new_team.ui")

class NewTeamDialog(QtBaseWindow, Ui_League_Manager_Main):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setStyleSheet("background-color: lightsteelblue;")
        self.setWindowIcon(QtGui.QIcon('img/stone.png'))


    def get_team_name(self):
        return self.new_team_line.text()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = NewTeamDialog()
    window.show()
    sys.exit(app.exec_())