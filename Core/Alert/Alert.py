import datetime

class Alert(object):

    def __init__(self,fid_patient):
        self.fid_patient = fid_patient
        self.fid_doctor = None
        self.date_contact = datetime.datetime.now()
        self.comment = ""
        self.is_booked = False
        self.score_consultation = 0

