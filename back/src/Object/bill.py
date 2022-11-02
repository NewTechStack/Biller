from .CRUD import Crud
from .timesheet import Timesheet
import requests
import uuid
from datetime import datetime
import json

class Bill(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'bill')

    def new(self, client_id, folder_id):
        bill_id = str(uuid.uuid4())
        self.id = f"{client_id}/{folder_id}/{bill_id}"
        return [True, {}, None]
    
    def status_0(self):
        ret = self.get()
        if ret[1] is None:
            retun [False, "error", 500]
        if int(ret[1]["status"]) != 0:
            return [False, "Operation only available if status == 0", 400]
        return [True, {}, None]
    
    def change_status(self, status):
        if status not in [0, 1, 2, 3, 4]:
            return [False, f"Status '{status}' not in range(0, 4)", 400]
        ret = self.get()
        if ret[1] is None:
            retun [False, "error", 500]
        if int(ret[1]["status"]) > status:
            return [False, "Can't revert status", 401]
        if int(ret[1]["status"]) + 1 != status:
            return [False, "Can't skip status", 401]
        return self._push({'status': status})

    def edit(self, data):
        data['id'] = self.id
        if not "lang" in data or data["lang"] not in ["fr", "en"]:
            return [False, "Invalid 'lang', 'fr' or 'en' only", 400]
        if not "type" in data or data["type"] not in ["invoice", "provision", "retainer"]:
          return [False, "Invalid 'type' of bill", 404]
        if not "TVA" in data or not any([isinstance(data["TVA"], x) for x in [float, int]]):
          return [False, "Invalid 'TVA' float", 400]
        tva = data["TVA"]
        data["TVA"] = float(data["TVA"])
        if not "TVA_inc" in data or not isinstance(data["TVA_inc"], bool):
          return [False, "Invalid 'TVA_inc' bool", 400]
        data["TVA_inc"] = bool(data["TVA_inc"])
        if data["type"] == "invoice":
            ret = self.__invoice(data)
            if ret[0] is False:
                return ret
            data = ret[1]
        if data["type"] == "provision":
            ret = self.__provision(data)
            if ret[0] is False:
                return ret
            data = ret[1]
        data["status"] = 0
        return self._push(data)
    
    def __provision(self, data):
        if not "prov_amount" in data or not any([isinstance(data["prov_amount"], x) for x in [float, int]]):
            return [False, "Invalid 'prov_amount' float or int", 400]
        prov_amount = data["prov_amount"]
        data["price"] = {
            "HT": self.__HT_price(float(prov_amount), data["TVA"], data["TVA_inc"]),
            "taxes": 0.0, 
            "total": 0.0
        }
        ret = self.__calc__fees(data)
        if ret[0] is False:
            return ret
        data = ret[1]
        ret = self.__calc_reductions(data)
        if ret[0] is False:
            return ret
        data = ret[1]
        data["price"]["HT"] = round(data["price"]["HT"], 2)
        data["price"]["taxes"] = round(self.__taxe(data["price"]["HT"], data["TVA"]), 2)
        data["price"]["total"] = data["price"]["HT"] + data["price"]["taxes"]
        return [True, data, None]
    
    def __invoice(self, data):
        if not "timesheet" in data or not isinstance(data["timesheet"], list) or not all([isinstance(x, str) for x in data['timesheet']]):
            return [False, "Invalid 'timesheet' list", 400]
        timesheets = data["timesheet"]
        if len(timesheets) == 0:
            return [False, "Invalid 'timsheet' list", 400]
        if len(timesheets) != len(set(timesheets)):
            return [False, "Duplicates in 'timesheet' list", 400]
        base_id = self.id.rsplit('/', 1)[0]
        data["price"] = {"HT": 0.0, "taxes": 0.0, "total": 0.0}
        lines = []
        for t_id in timesheets:
            ret = self.__calc_timesheet(f"{base_id}/{t_id}", data)
            if ret[0] is False:
                return ret
            lines.append(ret[1])
            data["price"]["HT"] += ret[1]["price_HT"]
        ret = self.__calc__fees(data)
        if ret[0] is False:
            return ret
        data = ret[1]
        ret = self.__calc_reductions(data)
        if ret[0] is False:
            return ret
        data = ret[1]
        data["price"]["HT"] = round(data["price"]["HT"], 2)
        data["price"]["taxes"] = round(self.__taxe(data["price"]["HT"], data["TVA"]), 2)
        data["price"]["total"] = data["price"]["HT"] + data["price"]["taxes"]
        data["timesheet"] = lines
        url = "http://template:8080/template/pdf"
        number = 1
        payload = {
            "name": f"invoice{data['lang']}.html",
            "title": f"{base_id}/facture_{number}",
            "variables": {
                "lines": data["timesheet"],
                "num": "0",
                "date": datetime.now().strftime("%d/%m/%Y"),
                "name": "TEST FACTURE",

                "timesheet_sum": sum(t["price_HT"] for t in data["timesheet"]), 
                "fees_percent": data["fees"]["fees"] if "fees" in data else 0,
                "fees_price_ht": data["fees"]["price_HT"] if "fees" in data else 0,

                "reduction_amount": "0",
                "reduction_unit": "%",
                "reduction_value": 0,

                "tva_amount": data["TVA"],
                "tva_value": data["price"]["taxes"],

                "provision": "0.00",

                "retainer": "0.00", 

                "total_ttc": data["price"]["total"]
            }
        }
        headers = {
            'content-type': "application/json",
        }
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        data["url"] = response.text
        return [True, data, None]
    
    def __HT_price(self, price, tva, tva_incl):
        if tva_incl is True:
            price = price / (1+(tva/100))
        return price
    
    def __taxe(self, price, tva):
        return self.__percentage(price, tva)
    
    def __TTC_price(self, price, tva):
        return price + self.__taxe(price, tva)
    
    def __fees_price(self, price, tva):
        return self.__taxe(price, tva)
    
    def __percentage(self, total, percentage):
        return total * percentage / 100
   
    def __calc_timesheet(self, timsheet_id, data):
        d = Timesheet(timsheet_id).get()
        if d[1] is None:
            return [False, f"Invalid timesheet id: '{timsheet_id}'", 404]
        if "price" not in d[1] or not any([isinstance(d[1]["price"], x) for x in [int, float]]):
            return [False, f"Invalid price in timesheet: '{timsheet_id}'", 400]
        price_HT =  self.__HT_price(float(d[1]["price"]), data["TVA"], data["TVA_inc"])
        taxes = self.__taxe(price_HT, data["TVA"])
        line = {
            "timesheet_id": timsheet_id,
            "price_HT": round(price_HT, 2),
            "taxes": round(taxes, 2),
            "TVA": data["TVA"],
            "price": round(self.__TTC_price(price_HT, data["TVA"]) , 2),
            "activite": d[1]["desc"],
            "user": d[1]["created_by"],
            "time": d[1]["duration"],
            "date": datetime.utcfromtimestamp(d[1]["date"]).strftime('%d/%m/%Y')
        }
        return [True, line, None]
    
    def __calc__fees(self, data):
        if "fees" in data:
            if not any([isinstance(data["fees"], x) for x in [float, int]]) and data["fees"] > 0.0:
                return [False, "Invalid fees value, float", 400]
            price_HT = self.__fees_price(data["price"]["HT"], data["fees"])
            data["fees"] = {
                "fees": data["fees"],
                "price_HT": round(price_HT, 2),
                "taxes": round(self.__taxe(price_HT, data["TVA"]), 2),
                "TVA": data["TVA"],
                "price": round(self.__TTC_price(price_HT, data["TVA"]), 2)
            }
            data["price"]["HT"] += price_HT
        return [True, data, None]
    
    def __calc_reductions(self, data):
        if "reduction" in data:
            if "fix" in data["reduction"]:
                if not any([isinstance(data["reduction"]["fix"], x) for x in [float, int]]):
                    return [False, "Invalid reduction.fix float", 400]
                taxes = self.__taxe(data["reduction"]["fix"], data["TVA"])
                price = self.__HT_price(data["reduction"]["fix"], data["TVA"], data["TVA_inc"])
                data["reduction"]["fix"] = {
                    "amount": data["reduction"]["fix"],
                    "value_HT": round(price, 2)
                }
                data["price"]["HT"] -= price
            if "percentage" in data["reduction"]:
                if not any([isinstance(data["reduction"]["percentage"], x) for x in [float, int]]):
                    return [False, "Invalid reduction.percentage float", 400]
                price = self.__percentage(data["price"]["HT"], data["reduction"]["percentage"])
                data["reduction"]["percentage"] = {
                    "amount": data["reduction"]["percentage"],
                    "value_HT": round(price, 2)
                }
                data["price"]["HT"] -= price
        return [True, data, None]
