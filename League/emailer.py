import datetime
import yagmail
"""
Emailer -- a singleton --  (file name: emailer.py)

    class variable sender_address
    class variable _sole_instance -- the only instance of this class
    class method configure(sender_address) -- sets the class variable as specified
    class method instance() -- return the only instance of this class
    send_plain_email(recipients, subject, message) -- Note: this is an instance method. 
     recipients must be a collection of email addresses (not TeamMembers!).  subject and message are strings.  
     Just have this method print f"Sending mail to: {recipient}" for each recipient in the recipients list. 
     We'll cover sending e-mail from Python later.
     
     Updated with yagmail support 04.13.2024
"""


class Emailer:

    sender_address = None
    _sole_instance = None
    _yag = None

  

    @classmethod
    def configure(cls, sender_address = 'jugray@gmail.com'):
        """
        Configured using keyring and Google app passwords
        https://support.google.com/accounts/answer/185833?hl=en
        If no email address is provided we will assume the default
        email address is 'jugray@gmail' which has the password registered
        in the system keyring.
        """
        cls.sender_address = sender_address
        cls.yag = yagmail.SMTP(cls.sender_address)

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, email):
        for player in recipients:
            print(f"""
Sending email to: {player}
Subject {subject}:
Body {email}""")
            self.yag.send(player, subject, email)

"""
    def yagTest(self):
        Yagmail test function run by main outside of League functions
        emailString= f"This is a test email dated {datetime.datetime.now()} from the League Emailer powered by Yagmail!"
        self.yag.send('redapex1029@gmail.com', 'Yagmail Emailer Test', emailString)
        print(f"Test email sent successfully from {testEmail.sender_address}!")
"""

if __name__ == '__main__':
    import datetime
    Emailer.configure('jugray@gmail.com')
    testEmail = Emailer.instance()
    #testEmail.yagTest()
    testEmail.send_plain_email(['redapex1029@gmail.com'], 'League Emailer Test','This email '
                                                                                'was sent from send_plain_email()')
