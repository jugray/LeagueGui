from GUI.League.identified_object import IdentifiedObject
from GUI.League.DuplicateOid import DuplicateOid

"""
League(IdentifiedObject)   (file name: league.py)

    name [prop] -- the league name teams [r/o prop] -- list of teams participating in this league competitions [r/o 
    prop] -- list of competitions (games) __init__(oid, name) -- initialization method that sets the oid and name 
    properties as specified in the arguments (note: should call superclass constructor) add_team(team) -- add team to 
    the teams collection unless they are already in it (in which case do nothing) remove_team(team) -- remove the 
    team if they are in the teams list, otherwise do nothing team_named(team_name) -- return the team in this league 
    whose name equals team_name (case sensitive) or None if no such team exists add_competition(competition) -- add 
    competition to the competitions collection teams_for_member(member) -- return a list of all teams for which 
    member plays competitions_for_team(team) -- return a list of all competitions in which team is participating 
    competitions_for_member(member) -- return a list of all competitions for which member played on one of the 
    competing teams __str__() -- return a string resembling the following: "League Name: N teams, M competitions" 
    where N and M are replaced by the obvious values

"""


class League(IdentifiedObject):

    def __init__(self, oid, nameIn) -> None:
        super().__init__(oid)
        self.name = nameIn
        self._teams = []
        self._competitions = []

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def add_team(self, teamIn):
        if teamIn is not None:
            if teamIn not in self._teams:
                self._teams.append(teamIn)
                return True
            else:
                raise DuplicateOid(teamIn._oid)
        else:
            return False

    def remove_team(self, teamIn):
        if teamIn is not None and len(self._teams) > 0:
            if teamIn in self._teams:
                for competition in self._competitions:
                    if teamIn not in competition._teams_competing:
                        raise ValueError
                self._teams.remove(teamIn)
                return True
        return False

    def team_named(self, teamIn):
        for team in self._teams:
            if team.name == teamIn:
                return team
        return None

    def add_competition(self, competition):
        for team in competition._teams_competing:
            if team not in self._teams:
                raise ValueError
        if competition not in self._competitions:
            self._competitions.append(competition)
            return True
        else:
            raise DuplicateOid("Duplicate oid in collection!")

    def teams_for_member(self, memberIn):
        teamList = []
        for team in self._teams:
            if team.member_named(memberIn.name) is not None:
                teamList.append(team)
        return teamList

    def competitions_for_team(self, teamIn):
        teamCompList = []
        for competition in self._competitions:
            if teamIn in competition._teams_competing:
                teamCompList.append(competition)
        return teamCompList

    def competitions_for_member(self, memberIn):
        compList = []
        for competition in self._competitions:
            teamList = competition._teams_competing
            for team in teamList:
                if team.member_named(memberIn.name) is not None:
                    compList.append(competition)
        return compList

    def __str__(self):
        return f"""
{self.name}: {len(self._teams)} teams, {len(self._competitions)}
"""
