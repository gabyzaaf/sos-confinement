CREATE_PATIENTS = """
    CREATE TABLE IF NOT EXISTS patients (
        id integer PRIMARY KEY autoincrement,
        name text,
        firstname text,
        email text,
        phone text,
        comment text,
        register_date timestamp
    );
"""

CREATE_USERS = """
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY autoincrement,
        name text,
        firstname text,
        email text,
        login text,
        password text,
        token text,
        is_admin boolean,
        register_date timestamp
    );
"""

CREATE_DOCTORS = """
    CREATE TABLE IF NOT EXISTS doctors (
        id integer PRIMARY KEY autoincrement,
        name text,
        firstname text,
        adheli text,
        login text,
        password text,
        token text,
        email text,
        speciality text,
        is_valid boolean,
        register_date timestamp,
        fid_user int,
        foreign key(fid_user) references users(id)
    );
"""

CREATE_ALERT = """
    CREATE TABLE IF NOT EXISTS alerts (
        id integer PRIMARY KEY autoincrement,
        fid_patient int,
        fid_doctor int,
        date_contact timestamp,
        comment text,
        is_booked boolean,
        score_consultation int,
        foreign key(fid_patient) references patients(id),
        foreign key(fid_doctor) references doctors(id)
    ) 
"""

SQL_SELECT_ADMIN_EXIST = """
    SELECT count(*) from users where login='root'
"""

SQL_INSERT_ADMIN_USER = """
    INSERT INTO users (name, firstname, email, login, password, token, is_admin, register_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_INSERT_PATIENT = """
    INSERT INTO patients (name, firstname, email, phone, comment, register_date)
    VALUES (?, ?, ?, ?, ?, ?)
"""

SQL_INSERT_DOCTOR = """
    INSERT INTO patients (name, firstname, email, phone, comment, register_date)
    VALUES (?, ?, ?, ?, ?, ?)
"""

SQL_INSERT_DOCTOR = """
    INSERT INTO doctors (name, firstname, adheli, login, password, token, email, speciality, is_valid, register_date,
    fid_user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_INSERT_ALERT = """
    INSERT INTO alerts (fid_patient, date_contact, is_booked)
    values (?, ?, ?)
"""

SQL_UPDATE_ALERT = """        
    UPDATE alerts set fid_doctor=?, date_contact=?, is_booked=? where id=?
"""

SQL_SELECT_DOCTORS = """
    SELECT id,email,name from doctors where is_valid = 1
"""