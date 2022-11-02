from bottle import route, run
import requests
import json
from jinja2 import Environment, BaseLoader, meta

class Template(Rethink):
    def __init__(self, name):
        super().__init__()
        self.conn = self.conn.table('template')
        self.name = name
        self.model = {
            "name": None,
            "template": None,
            "variables": {}
        }
        self.data = None
        self.loaded_template = None
        self.render = None

    def list(self):
        ret = list(
                self.conn.map(
                    lambda doc: doc['name']
                ).run()
              )
        return [True, ret, None]

    def get(self):
        if not self.__exist():
            return [False, "Template doesn't exist", 404]
        return [True, self.data, None]

    def new(self, template):
        if self.__exist():
            return [False, "Template name already exist", 401]
        variables = meta.find_undeclared_variables(
                        Environment().parse(
                            template
                        )
                    )
        data = self.model
        data['name'] = self.name
        data['template'] = template
        data['variables'] = variables
        self.conn.insert([data]).run()
        return [True, {'name': self.name}, None]

    def customize(self, vars, end = True):
        if not self.__exist():
            return [False, "Template doesn't exist", 404]
        if not self.__load():
            return [False, "Error loading tempalte", 500]
        for var in self.data['variables']:
            if var not in vars:
                return [False, f"Missing {var} in variables", 400]
        if not self.__render(vars):
            return [False, "Error rendering template", 500]
        return [True, self.render, None]

    def __render(self, vars):
        if self.loaded_template is None:
            return False
        self.render = self.loaded_template.render(**vars)
        return True

    def __load(self):
        if self.data is None or 'template' not in self.data:
            return False
        self.loaded_template = Environment(loader=BaseLoader).from_string(self.data['template'])
        return True

    def __exist(self):
        res = list(self.conn.filter(lambda doc: doc['name'] == self.name).run())
        if len(res) > 0:
            self.data = res[0]
            return True
        return False

class Pdf():
    def __init__(self):
        self.data = None

    def generate(self, html, title):
        print(html)
        response = requests.request(
          "POST",
          "http://pdfgenerator:8080",
          headers = {
                'Content-Type': 'application/json'
                },
          data = json.dumps(
                {
                    "content": html,
                    "options":
                    {
                        "pageSize": "letter",
                        "title": title
                    }
                }
            )
        )
        return [True, response.content, None]


@route('/')
def index():
    return "working" 

run(host='0.0.0.0', port=8080)
