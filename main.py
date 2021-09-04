from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from PersonService import PersonService
from JobService import JobService
from urllib.parse import parse_qs, urlparse
import pyodbc

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


class handler(BaseHTTPRequestHandler):
    personService = PersonService(cursor)
    jobService = JobService(cursor)

    def do_GET(self):
        if self.path == '/people':
            self.do_People()
        if self.path.__contains__('/job'):
            self.do_Job()
        if self.path.__contains__('/company'):
            self.do_Company()

    def do_POST(self):
        if self.path == '/person':
            self.do_Person()

    def do_Person(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)

        person = json.loads(post_body)
        print(person)
        self.personService.save_person(person)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_People(self):
        peopleDict = self.personService.get_people()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(peopleDict).encode(encoding='utf_8'))

    def do_Job(self):
        id = parse_qs(urlparse(self.path).query)["id"]
        jobDict = self.jobService.get_job(id)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(jobDict).encode(encoding='utf_8'))


server = HTTPServer(('localhost', 8080), handler)
server.serve_forever()
