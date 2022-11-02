import os
from bottle import route, run
import requests
import json
from jinja2 import Environment, BaseLoader, meta


class Template():
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

@route('/templates')
def index():
    source = "./source/"
    template_list = [f for f in os.listdir(source) if not os.path.isfile(os.path.join(source, f))]
    templates = {}
    for template in template_list:
        path = os.path.join(source, template, "template.html")
        if os.path.exists(path) and os.path.isfile(path):
            f = open(path, "r")
            templates[template] = {
                 "variables": meta.find_undeclared_variables(
                        Environment().parse(
                            str(f.read())
                        )
                    )
            }
            f.close()
    return [tempalte_list, templates]

run(host='0.0.0.0', port=8080)
