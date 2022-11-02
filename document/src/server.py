import os
from bottle import route, run, request, response
import requests
import json
from bottle import static_file
from jinja2 import Environment, BaseLoader, meta

@route('/')
def index():
    return "working" 

@route('/static/<template>/<filename>')
def server_static(template, filename):
    return static_file(filename, root=os.path.join("./source", template))

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
                 "variables": 
                    list(
                        meta.find_undeclared_variables(
                            Environment().parse(
                                str(f.read())
                            )
                        )
                    )
            }
            f.close()
    return json.dumps(templates)

@route('/template/html', 'POST')
def index():
    source = "./source/"
    name = request.json.get("name", None)
    variables = request.json.get("variables", {})
    if name is None:
        return "err1"
    path = os.path.join(source, name, "template.html")
    if not os.path.exists(path) or not os.path.isfile(path):
        return "err2"
    f = open(path, "r")
    template_str = str(f.read())
    f.close()
    template =  Environment(loader=BaseLoader).from_string(template_str)
    return template.render(**variables)

@route('/template/pdf', 'POST')
def index():
    source = "./source/"
    name = request.json.get("name", None)
    title = request.json.get("title", "facture")
    variables = request.json.get("variables", {})
    if name is None:
        return "err1"
    path = os.path.join(source, name, "template.html")
    if not os.path.exists(path) or not os.path.isfile(path):
        return "err2"
    f = open(path, "r")
    template_str = str(f.read())
    f.close()
    template =  Environment(loader=BaseLoader).from_string(template_str)
    html = template.render(**variables)
    print("ok1")
    pdf = requests.request(
          "POST",
          "http://pdfgenerator:8080",
          headers = {
                'Content-Type': 'application/json'
                },
          data = json.dumps(
                {
                    "content": '<HTML><head></head><body>test<img style="position:absolute;top:4.13in;left:0.91in;width:7.21in;height:0.28in" src="http://template:8080/static/facture_fr/ci_3.png" /></body></HTML>',
                    "options":
                    {
                        "pageSize": "letter",
                        "title": title
                    }
                }
            )
        )
    print("ok2")
    response.content_type = "application/pdf; charset=UTF-8"
    response.set_header("Content-Disposition", f"attachment; filename={title}.pdf")
    return pdf.content

@route('/template/pdf/url', 'POST')
def index():
    source = "./source/"
    name = request.json.get("name", None)
    variables = request.json.get("variables", {})
    if name is None:
        return "err1"
    path = os.path.join(source, name, "template.html")
    if not os.path.exists(path) or not os.path.isfile(path):
        return "err2"
    f = open(path, "r")
    template_str = str(f.read())
    f.close()
    template =  Environment(loader=BaseLoader).from_string(template_str)
    return template.render(**variables)

run(host='0.0.0.0', port=8080)
