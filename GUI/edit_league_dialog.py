import sys
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

from new_team import NewTeamDialog
from edit_team_dialog import EditTeamDialog
from GUI.League.team import Team

"""
 League editor shows list of teams in the league being edited.  Has import/export menu items or buttons that raise 
    Qt5 dialogs to select files for import/exports.  Has buttons to:
        Delete a team
        Add a team (the team name can be input directly in this window)
        Edit a team
"""

Ui_League_Manager_Main, QtBaseWindow = uic.loadUiType("edit_league_dialog.ui")

class EditLeagueDialog(QtBaseWindow, Ui_League_Manager_Main):
    def __init__(self, league_db = None, league = None,parent=None,):
        super().__init__(parent)
        self.setupUi(self)
        self.league_db = league_db
        self.league = league
        self.add_team_button.clicked.connect(self.add_team)
        self.edit_team_button.clicked.connect(self.edit_team)
        self.delete_team_button.clicked.connect(self.delete_team)
        self.import_csv_button.clicked.connect(self.import_csv)
        self.export_csv_button.clicked.connect(self.export_csv)
        self.setStyleSheet("background-color: lightsteelblue;")
        self.setWindowIcon(QtGui.QIcon('img/stone.png'))
        self.teams_list_widget.setStyleSheet("""
        background-image: url('img/stone.png');
        background-repeat: no-repeat;
        background-position: center;
        background-color: lightsteelblue;
        """)

        self.update_ui()

    def add_team(self):
        dialog = NewTeamDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_team = Team(self.league_db.next_oid(), dialog.get_team_name())
            self.league.add_team(new_team)
            self.update_ui()

    def edit_team(self):
        if len(self.league._teams) > 0:
            dialog = EditTeamDialog(self.get_selected_team(),self.league_db)
            dialog.exec_()
            self.update_ui()
        else:
            self.empty_list()
    def delete_team(self):
        if len(self.league._teams) > 0:
            self.league.remove_team(self.get_selected_team())
            self.update_ui()
        else:
            self.empty_list()

    def import_csv(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Import CSV',None, 'CSV Files (*.csv)')
        if file_name[0] == "":
            return
        self.league_db.import_league_teams(self.league, file_name[0])
        print ("Loaded CSV file: ", file_name[0])
        self.update_ui()

    def export_csv(self):
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Export CSV',None, 'CSV Files (*.csv')
        if file_name[0] == "":
            return
        self.league_db.export_league_teams(self.league, file_name[0])
        print ("Saved CSV file: ", file_name[0])
        self.update_ui()

    def get_selected_team(self):
       return self.league._teams[self.teams_list_widget.currentRow()]

    def empty_list(self):
        dialog = QMessageBox(QMessageBox.Icon.Warning,
                             "Warning!",
                             "Please add an item to edit.",
                             QMessageBox.StandardButton.Ok)
        dialog.exec_()
    def update_ui(self):
        self.teams_list_widget.clear()
        for team in self.league._teams:
            self.teams_list_widget.addItem(str(team))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EditLeagueDialog()
    window.show()
    window.update_ui()
    sys.exit(app.exec_())