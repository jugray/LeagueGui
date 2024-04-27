import sys
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

from League.team_member import TeamMember

Ui_League_Manager_Main, QtBaseWindow = uic.loadUiType("edit_team_dialog.ui")

"""
    Team editor shows list of team members in the team being edited.  Has buttons to
        Delete a member
        Add a member (the member's name and email can be input directly in this window)
        Update a member (the member's name and email can be input directly in this window)
"""

class EditTeamDialog(QtBaseWindow, Ui_League_Manager_Main):

    edit_mode = False

    def __init__(self, team = None,league_db = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.save_member_button.clicked.connect(self.save_member_clicked)
        self.edit_team_member_button.clicked.connect(self.edit_member_clicked)
        self.delete_member_button.clicked.connect(self.delete_member_clicked)
        self.team_in = team
        self.league_db = league_db
        self.setStyleSheet("background-color: lightsteelblue;")
        self.setWindowIcon(QtGui.QIcon('img/stone.png'))
        self.teams_roster_widget.setStyleSheet("""
        background-color: lightsteelblue;
        """)

        if self.team_in:
           self.updateUI()

    def save_member_clicked(self, team_member = None):
        player_name =self.player_name_line.text()
        player_email =self.player_email_line.text()
        if self.edit_mode:
            self.get_selected_member().name = player_name
            self.get_selected_member().email = player_email
            self.edit_mode = False
            print("Updating team member " + str(self.get_selected_member()))
        else:
            new_member = TeamMember(self.league_db.next_oid(),player_name,player_email)
            self.team_in.add_member(new_member)
            print("Adding new team member " + str(new_member))
        self.updateUI()

    def edit_member_clicked(self):
        if len(self.team_in._members) > 0:
            self.player_name_line.setText(self.get_selected_member().name)
            self.player_email_line.setText(self.get_selected_member().email)
            self.edit_mode = True
        else:
            self.empty_list()

    def delete_member_clicked(self):
        if len(self.team_in._members) > 0:
            print("Deleting team member " + str(self.get_selected_member()))
            self.team_in.remove_member(self.get_selected_member())
            self.updateUI()
        else:
            self.empty_list()


    def get_selected_member(self):
       return self.team_in._members[self.teams_roster_widget.currentRow()]

    def empty_list(self):
        dialog = QMessageBox(QMessageBox.Icon.Warning,
                             "Warning!",
                             "Please add an item to edit.",
                             QMessageBox.StandardButton.Ok)
        dialog.exec_()
    def updateUI(self):
        self.teams_roster_widget.clear()
        for member in self.team_in._members:
            self.teams_roster_widget.addItem(str(member))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EditTeamDialog()
    window.show()
    sys.exit(app.exec_())