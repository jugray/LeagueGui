import sys
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox
from edit_league_dialog import EditLeagueDialog
from new_league import NewLeagueDialog


from League.league_database import LeagueDatabase
from League.league import League

"""
    Create a PyQt5 interface for the Curling League Manager.  Your interface must include the following windows:

    Main window shows list of leagues in the current database.  Has load/save menu items and/or buttons that raise Qt5 
    file dialogs to select the file to load/save.  Has buttons to:
        Delete a league
        Add a league (the league name can be input directly in this window)
        Edit a league
   


Your editors can be modal or not, your choice, but if you use non-modal windows, be careful to properly handle loading 
a new database (it should close all editor windows except the main window).
"""

Ui_League_Manager_Main, QtBaseWindow = uic.loadUiType("main_window.ui")

class MainWindow(QtBaseWindow, Ui_League_Manager_Main):

    league_db = LeagueDatabase.instance()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.new_league_button.clicked.connect(self.new_league)
        self.edit_league_button.clicked.connect(self.edit_league)
        self.remove_league_button.clicked.connect(self.delete_league)
        self.action_save_league.triggered.connect(self.save_league)
        self.action_load_league.triggered.connect(self.load_league)
        self.setStyleSheet("background-color: lightsteelblue;")
        self.setWindowIcon(QtGui.QIcon('img/stone.png'))
        self.league_list.setStyleSheet("""
background-image: url('img/stone.png');
background-repeat: no-repeat;
background-position: center;
background-color: lightsteelblue;
""")

    def save_league(self):
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Database', None, 'LDB Files (*.ldb)')
        if file_name[0] == "":
            return
        self.league_db.save(file_name[0])
        self.update_ui()
        print("Saving league..." + file_name[0])

    def load_league(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Database', None, 'LDB Files (*.ldb)')
        if file_name[0] == "":
            return
        self.league_db.load(file_name[0])
        self.league_db._sole_instance = LeagueDatabase.instance()
        self.update_ui()
        print("Loading league..." + file_name[0])

    def new_league(self):
        dialog = NewLeagueDialog()
        if dialog.exec_() == QDialog.DialogCode.Accepted:
            new_league = League(self.league_db.next_oid(),dialog.get_league_name())
            print("Created New League: ", str(new_league))
            self.league_db.add_league(new_league)
            self.update_ui()

    def edit_league(self):
        if len(self.league_db._leagues) > 0:
            dialog = EditLeagueDialog(self.league_db, self.get_selected_league())
            dialog.exec_()
            self.update_ui()
        else:
            self.empty_list()

    def delete_league(self):
        if len(self.league_db._leagues) > 0:
            self.league_db.remove_league(self.get_selected_league())
            self.update_ui()
        else:
            self.empty_list()
    def update_ui(self):
        self.league_list.clear()
        for league in self.league_db._leagues:
            self.league_list.addItem(str(league))

    def empty_list(self):
        dialog = QMessageBox(QMessageBox.Icon.Warning,
                             "Warning!",
                             "Please add an item to edit.",
                             QMessageBox.StandardButton.Ok)
        dialog.exec_()
    def get_selected_league(self):
       return self.league_db._leagues[self.league_list.currentRow()]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())