import os
from bottle import route, run, request, response
import requests
import json
from bottle import static_file
from jinja2 import Environment, BaseLoader, meta
from minio import Minio 
import io

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
    response.content_type = 'application/json'
    source = "./source/"
    name = request.json.get("name", None)
    title = request.json.get("title", "facture")
    variables = request.json.get("variables", {})
    if name is None:
        return False
    path = os.path.join(source, name, "template.html")
    if not os.path.exists(path) or not os.path.isfile(path):
        return False
    f = open(path, "r")
    template_str = str(f.read())
    f.close()
    template =  Environment(loader=BaseLoader).from_string(template_str)
    html = template.render(**variables)
    pdf = requests.request(
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
                        "encoding": "UTF-8",
                        "pageSize": "A4",
                        "title": title
                    }
                }
            )
        )
    client = Minio(
        endpoint="minio:8080",
        access_key="admin",
        secret_key="adminadmin",
        secure=False
    )
    if not client.bucket_exists("files"):
        client.make_bucket("files")
    client.put_object("files", 
        f"{title}.pdf",  
        data=io.BytesIO(pdf.content), 
        length=len(pdf.content),
        content_type='application/pdf'
    )
    return client.get_presigned_url("GET", "files", f"{title}.pdf").split("?")[0]

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
