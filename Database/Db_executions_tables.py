import sqlite3
from sqlite3 import Error
from flask import jsonify
from Database.Db import DATABASE_LOCATION
from Database.Db_Queries import CREATE_USERS, CREATE_DOCTORS, CREATE_ALERT, CREATE_PATIENTS, SQL_INSERT_PATIENT, \
    SQL_SELECT_ADMIN_EXIST, SQL_INSERT_ADMIN_USER, SQL_INSERT_DOCTOR, SQL_INSERT_ALERT, SQL_UPDATE_ALERT, \
    SQL_SELECT_DOCTORS
from Exceptions.AlertException import AlertException
from Exceptions.PatientException import PatientException
from Exceptions.TechnicalException import TechnicalException
import datetime
import hashlib


def create_table(connection, file_table):
    """
    This function is a generic function to create table
    :param connection: database connection
    :param file_table: sql instructions
    :return:
    """
    connection_verification(connection)
    try:
        cursor = connection.cursor()
        cursor.execute(file_table)
    except Error as e:
        if connection:
            connection.close()
        raise TechnicalException(e)


def create_table_patients(connection):
    """
    This function create table patient
    :param connection: database connection
    :return:
    """
    create_table(connection, CREATE_PATIENTS)


def create_table_users(connection):
    """
    This function create table users
    :param connection: database connection
    :return:
    """
    create_table(connection, CREATE_USERS)


def create_table_doctors(connection):
    """
    This function create table doctors
    :param connection: database connection
    :return:
    """
    create_table(connection, CREATE_DOCTORS)


def create_table_alerts(connection):
    """
    This function create table alerts
    :param connection: database connection
    :return:
    """
    create_table(connection, CREATE_ALERT)


def connection_verification(connection):
    """
    This function check if the connection is already opened
    :param connection:
    :return:
    """
    if not connection:
        raise Error("The connection is closed ")


def create_connection(database):
    """
    This function create connection or create a new file.
    :return: connection
    """
    if database is None:
        raise IOError("your path not exist ")
    conn = None
    try:
        conn = sqlite3.connect(database)
        print("The sqllite version is {} ".format(sqlite3.version))
    except Error as e:
        print(e)
    return conn


def close_connection(connection):
    """
    This function close the connection
    :param connection:
    :return:
    """
    if connection:
        connection.close()


def add_new_patient(patient):
    conn = None
    try:
        conn = create_connection(DATABASE_LOCATION)
        cur = conn.cursor()
        cur.execute(SQL_INSERT_PATIENT, (patient.name,
                                         patient.first_name,
                                         patient.email,
                                         patient.phone,
                                         patient.comment,
                                         datetime.datetime.now(),))
        patient_id = cur.lastrowid
        conn.commit()
        return patient_id
    except Error:
        raise PatientException(jsonify({
            'status': 'error',
            'message': 'Technical error'
        }))
    finally:
        if conn:
            conn.close()


def add_new_alert(alert):
    conn = None
    try:
        conn = create_connection(DATABASE_LOCATION)
        cur = conn.cursor()
        cur.execute(SQL_INSERT_ALERT, (alert.fid_patient,
                                         alert.date_contact,
                                         alert.is_booked,))
        alert_id = cur.lastrowid
        conn.commit()
        return alert_id
    except Error:
        raise PatientException(jsonify({
            'status': 'error',
            'message': 'Technical error'
        }))
    finally:
        if conn:
            conn.close()


def add_new_doctor(doctor):
    conn = None
    try:
        conn = create_connection(DATABASE_LOCATION)
        cur = conn.cursor()

        cur.execute(SQL_INSERT_DOCTOR, (doctor.name,
                                         doctor.firstname,
                                         doctor.adheli,
                                         doctor.login,
                                         doctor.password,
                                         doctor.token,
                                         doctor.email,
                                         doctor.speciality,
                                         doctor.is_valid,
                                         doctor.register_date,
                                         doctor.fid_user,))
        conn.commit()
    except Error:
        raise PatientException(jsonify({
            'status': 'error',
            'message': 'Technical error'
        }))
    finally:
        if conn:
            conn.close()


def admin_exist():
    conn = None
    try:
        conn = create_connection(DATABASE_LOCATION)
        cur = conn.cursor()
        cur.execute(SQL_SELECT_ADMIN_EXIST)
        number = int(cur.fetchone()[0])
        return number > 0
    except Error:
        raise PatientException(jsonify({
            'status': 'error',
            'message': 'Technical error'
        }))
    finally:
        if conn:
            conn.close()


def create_admin_user():
    hash_object = hashlib.sha384("toor".encode("utf-8"))
    pwd = hash_object.hexdigest()
    if not admin_exist():
        conn = None
        try:
            conn = create_connection(DATABASE_LOCATION)
            cur = conn.cursor()
            cur.execute(SQL_INSERT_ADMIN_USER, ("admin", "admin", "root@sos-confinement.fr", "root", pwd, "1234", 1, datetime.datetime.now(),))
            conn.commit()
        except Error:
            raise PatientException(jsonify({
                'status': 'error',
                'message': 'Technical error'
            }))
        finally:
            if conn:
                conn.close()


def book_alert(alert_id, doctor_id):
    conn = None
    try:
        conn = create_connection(DATABASE_LOCATION)
        cur = conn.cursor()
        cur.execute(SQL_UPDATE_ALERT, (doctor_id,
                                       datetime.datetime.now(),
                                       1,
                                       alert_id,))
        conn.commit()
    except Error:
        raise AlertException(jsonify({
            'status': 'error',
            'message': 'Technical error'
        }))
    finally:
        if conn:
            conn.close()


def get_doctors():
    conn = None
    try:
        conn = create_connection(DATABASE_LOCATION)
        cur = conn.cursor()
        cur.execute(SQL_SELECT_DOCTORS)
        doctors = cur.fetchall()
        return doctors
    except Error:
        raise AlertException(jsonify({
            'status': 'error',
            'message': 'Technical error'
        }))
    finally:
        if conn:
            conn.close()


def db_init_locally():
    """
    This function initialize all the tables
    :return:
    """
    conn = None
    try:
        conn = create_connection(DATABASE_LOCATION)
        create_table_patients(conn)
        create_table_users(conn)
        create_table_doctors(conn)
        create_table_alerts(conn)
        create_admin_user()
    except Error :
        return jsonify({
                    'status': 'error',
                    'message': "Technical error"
                })
    finally:
        close_connection(conn)