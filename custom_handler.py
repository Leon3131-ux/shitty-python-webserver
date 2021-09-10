from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json


def CustomHandlerFactory(person_service):
    class CustomHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.path == '/people':
                self.get_people()

        def do_POST(self):
            if self.path == '/person':
                self.save_person()

        def do_DELETE(self):
            if self.path.__contains__('/person'):
                self.delete_person()

        def save_person(self):
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            print(post_body)

            person = json.loads(post_body)
            print(person)
            person_service.save_person(person)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

        def get_people(self):
            people_dict = person_service.get_people()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(people_dict).encode(encoding='utf_8'))

        def delete_person(self):
            parsed_url = urlparse(self.path)
            person_id = parse_qs(parsed_url.query)['id'][0]
            person_service.delete_person(person_id)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

    return CustomHandler
