import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Exceptions.TechnicalException import TechnicalException

GMAIL_PWD = "pwd"
SENDER = "from"
RECEIVER = "to"
CONTENT = "content"

PORT=587
SMTP="smtp.gmail.com"
PWD = "EyP@ssword2020"


def create_format(sender, receiver, email):
    """
    this function create the email format to send.
    :param sender: who send the email
    :param receiver: who will receive the email
    :param email: contains the email informations (body + subject)
    :return: dictionary with the sender, receiver and email formatted
    """
    email_information = {}
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = email.subject
    email_content = MIMEText(email.body, 'plain')
    msg.attach(email_content)
    email_information[GMAIL_PWD] = PWD
    email_information[SENDER] = sender
    email_information[RECEIVER] = receiver
    email_information[CONTENT] = msg.as_string()
    return email_information


def verifications_inputs(input, error_message):
    if not input or input == "":
        raise TechnicalException(error_message)


def sender_email(sender, receiver, subject_body):
    """
    This function send the email to the receiver
    :param sender: email sender
    :param receiver: email receiver
    :param subject_body : email subject and content
    :return:
    """
    server = ""
    try:
        verifications_inputs(sender, "Your sender is not good ")
        verifications_inputs(receiver, "Your receiver is not good ")
        verifications_inputs(subject_body, "Your subject_body is not good ")
        email_information = create_format(sender, receiver, subject_body)
        server = smtplib.SMTP(SMTP, PORT)
        server.ehlo()
        server.starttls()
        server.login(email_information[SENDER], email_information[GMAIL_PWD])
        server.sendmail(email_information[SENDER],email_information[RECEIVER],email_information[CONTENT])
        print("The email was send {}".format(email_information[RECEIVER]))
    except TechnicalException as technic:
        raise technic
    finally:
        if server:
            server.close()

