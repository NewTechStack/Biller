from .rethink import get_conn, r
import requests
import uuid
from datetime import datetime
import json

class Report():
    def __init__(self, id = None):
        self.rt = get_conn().db("ged").table("timesheet")
        
    def __currency_format(self, price):
        return f"{price:_.2f}".replace(".00", ".-").replace("_", " ")
    
    def __hours_format(self, hours):
        return f"{hours:_.2f}".split(".")[0] + "h"
    
    def get(self, start = 0, end=1670239999, user = "ca1e6590-47d9-4ee0-ba9f-533c1de65325"):
        
        lines = []
        base = self.rt.filter({"status": 0, "user": user}).filter(lambda timesheet: timesheet["date"] >= start & timesheet["date"] <= end)
        damn = sum([d["duration"] for d in list(base.pluck(["duration"]).run())])
        paid_price = 10000
        billed_price = 1000
        non_price = 200
        total = paid_price + billed_price + non_price
        time = 10
        lines.append({
                        "name": "test",
                        "avg_price": self.__currency_format(total/time) + " CHF",
                        
                        "paid_perc": int(f"{paid_price*100/total:_.0f}"),
                        "paid_price": self.__currency_format(paid_price) + " CHF",
                        "paid_price_raw": paid_price,
                        
                        "billed_perc": int(f"{billed_price*100/total:_.0f}"),
                        "billed_price": self.__currency_format(billed_price) + " CHF",
                        "billed_price_raw": billed_price,
                        
                        "non_perc": int(f"{non_price*100/total:_.0f}"),
                        "non_price": self.__currency_format(non_price) + " CHF",
                        "non_price_raw": non_price,
                        
                        "time":  self.__hours_format(time),
                        "time_raw": time,
            
                        "total_raw": total
                    })
        total_hours = sum([line["time_raw"] for line in lines])
        
        url = "http://template:8080/template/pdf"
        data = {
            "name": f"report.html",
            "title": f"damn",
            "bucket": "reports",
            "variables": {
                "name": "Eliot Dujardin",
                "total_hours": self.__hours_format(total_hours),
                "total_priced": self.__currency_format(sum([line["total_raw"] for line in lines])) + " CHF",
                "avg_price": self.__currency_format(sum([line["total_raw"] for line in lines]) / (total_hours if total_hours > 0 else 1)) + " CHF",
                "total_payed": self.__currency_format(sum([line["paid_price_raw"] for line in lines])) + " CHF",
                "lines": lines,
            }
        }
        response = requests.request("POST", url, data=json.dumps(data), headers={'content-type': "application/json"})
        return [True, {"url": json.loads(response.text), "data": damn}, 200]
      
