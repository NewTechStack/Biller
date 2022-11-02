from bottle import route, run
import requests
import json

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
