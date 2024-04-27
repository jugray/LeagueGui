from League.identified_object import IdentifiedObject

"""
TeamMember(IdentifiedObject) --  (file name: team_member.py)

    name [prop] email [prop] __init__(oid, name, email)-- initialization method that sets the oid, name and email
    properties as specified in the arguments (note: should call superclass constructor) send_email(emailer,
    subject, message) -- use the emailer argument to send an email to to this member __str__() -- return a string
    like the following: "Name<Email>"
"""

class TeamMember(IdentifiedObject):

    def __init__(self, oid, name, email):
        super().__init__(oid)
        self.name = name
        self.email = email

    def send_email(self, emailer, subject, message):
         emailer.send_plain_email([self.email], subject, message)


    def __str__(self):
        return f"{self.name}<{self.email}>"
