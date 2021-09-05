from http.server import HTTPServer

from company import CompanyService
from custom_handler import CustomHandlerFactory
import pyodbc

from department import DepartmentService
from job import JobService
from person import PersonService

connection_string = (
    'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
    'SERVER=localhost;'
    'DATABASE=m151;'
    'UID=root;'
    'PWD=root;'
    'charset=utf8mb4;'
)

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

job_service = JobService(cursor)
company_service = CompanyService(cursor)
department_service = DepartmentService(cursor)
person_service = PersonService(cursor, job_service, company_service, department_service)

custom_handler = CustomHandlerFactory(person_service)


server = HTTPServer(('localhost', 8080), custom_handler)
server.serve_forever()
