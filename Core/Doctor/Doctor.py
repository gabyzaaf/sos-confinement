import re
from Exceptions.DoctorException import DoctorException
import datetime
import hashlib

class Doctor(object):
    def __init__(self, name, firstname, adheli, login, password, token, email, speciality):
        self.name = name
        self.firstname = firstname
        self.adheli = adheli
        self.login = login
        self.password = password
        self.encode_pwd()
        self.token = token
        self.email = email
        self.speciality = speciality
        self.fid_user = 1
        self.is_valid = 1
        self.register_date = datetime.datetime.now()
        password = None

    def __valid_email(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(regex, self.email):
            raise DoctorException("Your email is null")

    def encode_pwd(self):
        hash_object = hashlib.sha384(self.password.encode("utf-8"))
        self.password = hash_object.hexdigest()
