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
    
    def __currency_format(self, price):
        return f"{price:_.2f}".replace(".00", ".-").replace("_", " ")
    
    def __hours_format(self, price):
        return f"{price:_.2f}".split(".")[0] + "h"
    
    def get(self):
        url = "http://template:8080/template/pdf"
        data = {
            "name": f"report.html",
            "title": f"damn",
            "bucket": "reports",
            "variables": {
                "name": "Eliot Dujardin",
                "total_hours": self.__hours_format(10),
                "total_priced": self.__currency_format(1999) + " CHF",
                "avg_price": self.__currency_format(300) + " CHF",
                "total_payed": self.__currency_format(1599) + " CHF",
                "lines": [
                    {
                        "name": "test",
                        "avg_price": self.__currency_format(300) + " CHF",
                        
                        "paid_percent": 80,
                        "paid_price": self.__currency_format(1999) + " CHF",
                        
                        "billed_percent ": 10,
                        "billed_price ": self.__currency_format(80) + " CHF",
                        
                        "non_percent": 10,
                        "non_price": self.__currency_format(80) + " CHF",
                        
                        "time":  self.__hours_format(10)
                    }
                ],
            }
        }
        response = requests.request("POST", url, data=json.dumps(data), headers={'content-type': "application/json"})
        return [True, json.loads(response.text), 200]
      
