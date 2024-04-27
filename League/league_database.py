import pickle
import csv
from League.team import Team
from League.team_member import TeamMember

class LeagueDatabase:

    _sole_instance = None
    _leagues = []
    _last_oid = 0

    def __init__(self):
        self._sole_instance = None
        self._leagues = []
        self._last_oid = 0

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name, mode="rb") as f:
                cls._sole_instance = pickle.load(f)
                print(f"Successfully loaded {file_name}")
        except FileNotFoundError:
            file_name = file_name + ".backup"
            print("No file found, trying backup.")
            with open(file_name, mode="rb") as f:
                cls._sole_instance = pickle.load(f)
                print(f"Successfully loaded {file_name}")

    @property
    def leagues(self):
        return self._leagues

    def add_league(self, league):
        self._leagues.append(league)
        return True

    def remove_league(self, league):
        if league in self._leagues:
            self._leagues.remove(league)
    
    def league_named(self, league_name):
        for current in self._leagues:
            if current.name == league_name:
                return current
        return None

    def next_oid(self):
        self._last_oid += 1
        return self._last_oid
    
    def save(self, file_name):
        try:
            with open(file_name, mode="xb") as f:
                pickle.dump(self._sole_instance, f)
        except FileExistsError:
            with open(str(file_name + ".backup"), mode="wb") as f:
                print(f"Warning! Duplicate file detected, saving file to {file_name}.backup!")
                pickle.dump(self._sole_instance,f)
                return

    def import_league_teams(self, league, file_name):
        current_team = None
        new_team = None
        row_count = 0
        try:
            with open(file_name, mode="r", encoding="utf8")as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    if row_count != 0:
                        if current_team != row[0]:
                            new_team = Team(self.next_oid(), row[0])
                            league.teams.append(new_team)
                            current_team = row[0]
                        new_team.add_member(TeamMember(self.next_oid(), row[1], row[2]))
                    row_count += 1

        except FileNotFoundError:
            raise FileNotFoundError(f"Error reading file {file_name}")

    def export_league_teams(self, league, file_name):
        header = ["Team name", "Member name", "Member email"]

        try:
            with open(file_name, mode="w", encoding="utf8", newline= '') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(header)
                for team in league.teams:
                    for team_member in team._members:
                        writer.writerow([team.name, team_member.name, team_member.email])
        except IOError:
            print("Error writing file")
