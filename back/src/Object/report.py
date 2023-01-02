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
            "bucket": "reports",
            "variables": {
                "name": "Eliot Dujardin",
                "lines": [
                    {
                        "name": "test",
                        "payed": 80,
                        "non_payed": 10,
                        "billed": 10,
                        "time": "10H30"
                    }
                ],
                "total": "300.- CHF",
                "total_payed": "30.- CHF"
            }
        }
        response = requests.request("POST", url, data=json.dumps(data), headers={'content-type': "application/json"})
        return [True, json.loads(response.text), 200]
      
