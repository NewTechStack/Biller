from .rethink import get_conn, r
import requests
import uuid
from datetime import datetime
import json
from math import ceil

class Report():
    def __init__(self, id = None):
        self.rt = get_conn().db("ged").table("timesheet")
        self.cl = get_conn().db("ged").table("client")
        self.fo = get_conn().db("ged").table("folder")
        
    def __currency_format(self, price):
        return f"{price:_.2f}".replace(".00", ".-").replace("_", " ")
    
    def __hours_format(self, hours):
        return f"{hours:_.2f}".split(".")[0] + "h"
    
    def get(self, start = 0, end=1670239999, user = "ca1e6590-47d9-4ee0-ba9f-533c1de65325"):
        
        lines = []
        clients = list(self.rt.filter({"user": user}).pluck("client_folder", "client").distinct().run())
        for i in clients:
            c_name = dict(self.cl.get(i["client"]).run())
            name = f"{c_name['name_1']} {c_name['name_2']}".strip()
            name += ": " + dict(self.fo.get(i["client_folder"]).run())["name"]
            paid_price = sum([d["price"] * d["duration"] for d in list(self.rt.filter({"status": 2, "user": user, "client_folder": i["client_folder"]}).filter(lambda timesheet: timesheet["date"] >= start & timesheet["date"] <= end).run())])
            billed_price = sum([d["price"] * d["duration"] for d in list(self.rt.filter({"status": 1, "user": user, "client_folder": i["client_folder"]}).filter(lambda timesheet: timesheet["date"] >= start & timesheet["date"] <= end).run())])
            non_price = sum([d["price"] * d["duration"] for d in list(self.rt.filter({"status": 0, "user": user, "client_folder": i["client_folder"]}).filter(lambda timesheet: timesheet["date"] >= start & timesheet["date"] <= end).run())])
            total = paid_price + billed_price + non_price
            time =  sum([d["duration"] for d in list(self.rt.filter({"user": user,  "client_folder": i["client_folder"]}).filter(lambda timesheet: timesheet["date"] >= start & timesheet["date"] <= end).pluck(["duration"]).run())])
            lines.append({
                        "name": name,
                        "avg_price": self.__currency_format(total/(time if time > 0 else 1)) + " CHF",
                        
                        "paid_perc": int(f"{paid_price*100/(total if total > 0 else 1):_.0f}"),
                        "paid_price": self.__currency_format(paid_price) + " CHF",
                        "paid_price_raw": paid_price,
                        
                        "billed_perc": int(f"{billed_price*100/(total if total > 0 else 1):_.0f}"),
                        "billed_price": self.__currency_format(billed_price) + " CHF",
                        "billed_price_raw": billed_price,
                        
                        "non_perc": int(f"{non_price*100/(total if total > 0 else 1):_.0f}"),
                        "non_price": self.__currency_format(non_price) + " CHF",
                        "non_price_raw": non_price,
                        
                        "time":  self.__hours_format(ceil(time)),
                        "time_raw": time,
            
                        "total_raw": total
                    })
        total_hours = sum([d["duration"] for d in list(self.rt.filter({"user": user}).filter(lambda timesheet: timesheet["date"] >= start & timesheet["date"] <= end).pluck(["duration"]).run())])
        
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
        return [True, {"url": json.loads(response.text), "data": data}, 200]
      
