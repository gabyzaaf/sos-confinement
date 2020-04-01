import datetime
import re
from Exceptions.PatientException import PatientException


class Patient(object):

    def __init__(self, name, first_name, email, phone, comment):
        self.name = name
        self.first_name = first_name
        self.email = email
        self.phone = phone
        self.comment = comment
        self.register_date = datetime.datetime.now()
        self.__valid_email()


    def __valid_email(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(regex, self.email):
            raise PatientException("Your email is null")


    def __valid_phone(self):
        if not self.phone or "":
            raise PatientException("Your phone is not valid")




