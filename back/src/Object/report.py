from .timesheet import Timesheet
from .folder import Folder
from .user import User
from .bank import Bank
import requests
import uuid
from datetime import datetime
import json

class Report():
    def __init__(self, id = None):
        pass
    
    def get(self):
        url = "http://template:8080/template/pdf"
        data = {
            "name": f"report.html",
            "title": f"damn",
            "variables": {}
        }
        response = requests.request("POST", url, data=json.dumps(data), headers={'content-type': "application/json"})
        return [True, json.loads(response.text), 200]
      
