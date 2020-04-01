from flask import Flask, request, jsonify

from Core.Alert.Alert import Alert
from Core.Doctor.Doctor import Doctor
from Core.Email.Email import sender_all_email
from Core.Patient.Patient import Patient
from Database.Db_executions_tables import db_init_locally, add_new_patient, add_new_doctor, add_new_alert, book_alert, \
    get_doctors
from Exceptions.PatientException import PatientException
from Exceptions.AlertException import AlertException
app = Flask(__name__)


@app.route('/patient_sos', methods=['POST'])
def patient_call():
    try:
        name = request.form["name"]
        firstname = request.form["firstname"]
        email = request.form["email"]
        phone = request.form["phone"]
        comment = request.form["comment"]
        patient_anonymous = Patient(name, firstname, email, phone, comment)
        patient_id = add_new_patient(patient_anonymous)
        alert = Alert(patient_id)
        alert_id = add_new_alert(alert)
        sender_all_email(alert_id)
        return jsonify({
            'status': 'succes',
            'message': 'Your urgence is in progress'
        })
    except PatientException as p:
        return str(p)


@app.route('/register_doctor', methods=['POST'])
def register_doctor():
    try:
        name = request.form["name"]
        firstname = request.form["firstname"]
        adheli = request.form["adheli"]
        login = request.form["login"]
        password = request.form["password"]
        token = request.form["token"]
        email = request.form["email"]
        speciality = request.form["speciality"]
        new_doctor = Doctor(name, firstname, adheli, login, password, token, email, speciality)
        add_new_doctor(new_doctor)
        return jsonify({
            'status': 'succes',
            'message': 'Doctor added'
        })
    except PatientException as p:
        return str(p)


@app.route('/book_patient/<int:alert_id>/<int:doctor_id>', methods=['GET'])
def book_patient(alert_id, doctor_id):
    try:
        book_alert(alert_id, doctor_id)
        return jsonify({
            'status': 'succes',
            'message': 'You booked the patient'
        })
    except AlertException as a:
        return str(a)





if __name__ == "__main__":
    db_init_locally()
    app.run(debug=False)
    app.run(host='0.0.0.0')