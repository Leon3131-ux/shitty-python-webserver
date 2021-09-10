from pyodbc import Cursor

from company import CompanyService
from department import DepartmentService
from job import JobService


class PersonService:

    def __init__(self, cursor: Cursor,
                 job_service: JobService,
                 company_service: CompanyService,
                 department_service: DepartmentService):
        self.cursor = cursor
        self.job_service = job_service
        self.company_service = company_service
        self.department_service = department_service

    def save_person(self, person):

        job = self.job_service.get_job_by_name(person["jobName"])
        company = self.company_service.get_company_by_name(person["companyName"])
        department = self.department_service.get_department_by_name(person["departmentName"], person["companyName"])
        if not job:
            job = self.job_service.save_job(person["jobName"])

        if not company:
            company = self.company_service.save_company(person["companyName"])
            department = self.department_service.save_department(person["departmentName"], company["id"],
                                                                 company["name"])
        else:
            if not department:
                department = self.department_service.save_department(person["departmentName"], company["id"],
                                                                     company["name"])

        self.cursor.execute("{CALL sp_savePerson(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)}",
                            (
                                person["id"],
                                person["firstname"],
                                person["surname"],
                                person["birthdate"],
                                person["email"],
                                person["ahvNumber"],
                                person["personalNumber"],
                                person["phoneNumber"],
                                job["id"],
                                department["id"]
                            )
                            )
        self.cursor.commit()

    def get_people(self):
        rows = self.cursor.execute("{CALL sp_getPeople()}")

        peopleDicts = []
        for row in rows:
            print(row)
            person = {
                "id": row.ID,
                "firstname": row.FIRSTNAME,
                "surname": row.SURNAME,
                "birthdate": row.BIRTHDATE.strftime('%m/%d/%Y'),
                "email": row.EMAIL,
                "ahvNumber": row.AHV_NUMBER,
                "personalNumber": row.PERSONAL_NUMBER,
                "phoneNumber": row.PHONE_NUMBER,
                "jobName": row.JOB_NAME,
                "departmentName": row.DEPARTMENT_NAME,
                "companyName": row.COMPANY_NAME
            }
            peopleDicts.append(person)

        return peopleDicts

    def delete_person(self, person_id):
        self.cursor.execute("{CALL sp_deletePerson(?)}", person_id)
        self.cursor.commit()
