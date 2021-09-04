from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse


def CustomHandlerFactory(person_service, job_service):

    class CustomHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.path == '/people':
                self.do_People()
            if self.path.__contains__('/job'):
                self.do_Job()
            # if self.path.__contains__('/company'):
            #     self.do_Company()

        def do_POST(self):
            if self.path == '/person':
                self.do_Person()

        def do_Person(self):
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            print(post_body)

            person = json.loads(post_body)
            print(person)
            person_service.save_person(person)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        def do_People(self):
            peopleDict = person_service.get_people()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(peopleDict).encode(encoding='utf_8'))

        def do_Job(self):
            id = parse_qs(urlparse(self.path).query)["id"]
            jobDict = job_service.get_job(id)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(jobDict).encode(encoding='utf_8'))

    return CustomHandler
