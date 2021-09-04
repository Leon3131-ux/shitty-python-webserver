from pyodbc import Cursor

connection_string = (
    'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
    'SERVER=localhost;'
    'DATABASE=m151;'
    'UID=root;'
    'PWD=root;'
    'charset=utf8mb4;'
)


class PersonService:
    cursor: Cursor = None

    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def save_person(self, person):
        self.cursor.execute("{CALL sp_savePerson(?, ?, ?, ?, ?, ?, ?, ?, ?)}",
                            (person["firstname"],
                             person["surname"],
                             person["birthdate"],
                             person["email"],
                             person["ahvNumber"],
                             person["personalNumber"],
                             person["phoneNumber"],
                             person["jobId"],
                             person["departementId"])
                            )
        self.cursor.commit()

    def get_people(self):
        self.cursor.execute("SELECT FIRSTNAME, "
                            "SURNAME, "
                            "BIRTHDATE, "
                            "EMAIL, "
                            "AHV_NUMBER, "
                            "PERSONAL_NUMBER, "
                            "PHONE_NUMBER, "
                            "JOB_ID, "
                            "DEPARTEMENT_ID FROM Person")
        rows = self.cursor.fetchall()
        peopleDicts = []
        for row in rows:
            print(row)
            person = {
                "firsname": row.FIRSTNAME,
                "surname": row.SURNAME,
                "birthdate": row.BIRTHDATE.strftime('%m/%d/%Y'),
                "email": row.EMAIL,
                "ahvNumber": row.AHV_NUMBER,
                "personalNumber": row.PERSONAL_NUMBER,
                "phoneNumber": row.PHONE_NUMBER,
                "jobId": row.JOB_ID,
                "departementId": row.DEPARTEMENT_ID
            }
            peopleDicts.append(person)

        return peopleDicts

