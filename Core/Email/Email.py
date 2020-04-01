from Core.Email.Email_sender import sender_email
from Database.Db_executions_tables import get_doctors

EMAIL = "custom.mon.email.3@gmail.com"

class Email_sended():

    def __init__(self, subject, body):
        self.__subject = subject
        self.__body = body

    @property
    def subject(self):
        return self.__subject

    @property
    def body(self):
        return self.__body

    def __repr__(self):
        return "subject : {} \n body : {} ".format( self.__subject, self.__body)


def body_generator(doctor_name, url):
    """
    This function generate a specific body
    :return:
    """
    subject = "New Patient for you"
    body = """
        Hello {} 
        
        You can book the patient here : 
        {}
        
        Best regards,

    """.format(doctor_name, url)
    return Email_sended(subject, body)


def sender_all_email(alert_id):
    doctors = get_doctors()
    for doctor in doctors:
        url = "http://127.0.0.1:5000/book_patient/{}/{}".format(alert_id, doctor[0])
        email_generator_sended(EMAIL, doctor[1], doctor[2], url)


def email_generator_sended(email_sender, email_receiver, doctor_name, url):
    """
    This function generate the email to send
    :param sender: sender name
    :param receiver: receiver name
    :param domain: receiver domain
    :param connection: database connection
    :return:
    """

    email_content = body_generator(doctor_name, url)
    sender_email(email_sender, email_receiver, email_content)
