from League.identified_object import IdentifiedObject

"""
Competition(IdentifiedObject) --  (file name: competition.py)

    teams_competing [r/o prop] -- list containing two teams that are competing against each other date_time [prop] -- 
    optional (may be None) -- a Python datetime objects (not a string!) indicating when the competition will begin. 
    location [prop]

    __init__(oid, teams, location, datetime) -- initialization method that sets the oid, teams, location and 
    date_time properties as specified in the arguments (note: should call superclass constructor).
     
    Note: teams should be a list.  See above for the type of the datetime argument.

    send_email(emailer, subject, message) -- use the emailer argument to send an email to all members of all teams in 
    this competition without duplicates. That is, a team member may be on multiple teams that may be competing 
    against each other.  Only send one email to each team member on all of the teams in this competition. This method 
    should send a single email so if the teams have N and M members respectively, the recipient list will have N+M 
    elements assuming all of the members were distinct. If the teams have S "shared" members then we'd expect a 
    single email with N+M-S recipients.

    __str__() -- return a string like the following: "Competition at location on date_time with N teams" (note: 
    date_time may be None in which case just omit the "on date_time" part.  If present, format the date_time property 
    similar to the following example "12/31/1995 19:30"."""


class Competition(IdentifiedObject):

    def __init__(self, oid, teamsIn, location, datetime = None) -> None:
        super().__init__(oid)
        self._teams_competing = teamsIn
        self.location = location
        self.date_time = datetime

    @property
    def teams_competing(self):
        return self._teams_competing

    def send_email(self, emailer, subject, message):
        emailList = []
        if len(self._teams_competing) > 0:
            for team in self._teams_competing:
                for player in team.members:
                    if player.email not in emailList:
                        emailList.append(player.email)
            emailer.send_plain_email(emailList, subject, message)

    def __str__(self):
        return f"Competition at {self.location}"
