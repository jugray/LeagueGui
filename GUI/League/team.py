from League.identified_object import IdentifiedObject
from League.DuplicateOid import DuplicateOid
from League.DuplicateEmail import DuplicateEmail

"""
Team(IdentifiedObject) --  (file name: team.py)

    name [prop] members [r/o prop] -- list of team members __init__(oid, name) -- initialization method that sets the 
    oid and name properties as specified in the arguments (note: should call superclass constructor) add_member(
    member) -- ignore request to add team member that is already in members member_named(s) -- return the member of 
    this team whose name equals s (case sensitive) or None if no such member exists remove_member(member) -- remove 
    the specified member from this team send_email(emailer, subject, message) -- use the emailer argument to send an 
    email to all members of a team except those whose email address is None.  This method should send a single email 
    so if the team has N members, the recipient list will have N elements. __str__() -- return a string like the 
    following: "Team Name: N members"""


class Team(IdentifiedObject):

    def __init__(self, oid, name) -> None:
        super().__init__(oid)
        self.name = name
        self._members = []

    @property
    def members(self):
        return self._members

    def add_member(self, member):
        if member is None:
            return False
        if member in self.members:
            raise DuplicateOid(member._oid)
        else:

            for current_members in self._members:
                if member.email.upper() == current_members.email.upper():
                    raise DuplicateEmail(member.email)
            self._members.append(member)
            return True

    def member_named(self, member_name):
        for player in self._members:
            if player.name == member_name:
                return player
        else:
            return None

    def remove_member(self, memberIn):
        if memberIn is not None and len(self.members) > 0:
            for player in self._members:
                if player.name == memberIn.name:
                    self._members.remove(player)
                    return True

        else:
            return False

    def send_email(self, emailer, subject, message):
        emailList = []
        for player in self._members:
            if player.email is not None:
                emailList.append(player.email)
        emailer.send_plain_email(emailList, subject, message)
        return len(emailList)

    def __str__(self):
        return f"{self.name}: {len(self._members)} members"
