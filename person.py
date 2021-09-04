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

    def __init__(self, cursor: Cursor, job_service):
        self.cursor = cursor
        self.job_service = job_service

    def save_person(self, person):

        job = self.job_service.get_job_by_name(person["jobName"])
        if not job:
            job = self.job_service.save_job(person["jobName"])

        self.cursor.execute("{CALL sp_savePerson(?, ?, ?, ?, ?, ?, ?, ?, ?)}",
                            (person["firstname"],
                             person["surname"],
                             person["birthdate"],
                             person["email"],
                             person["ahvNumber"],
                             person["personalNumber"],
                             person["phoneNumber"],
                             job["id"],
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

