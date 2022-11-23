from .CRUD import Crud, StatusObject
from .timesheet import Timesheet
from .folder import Folder
from .user import User
from .bank import Bank
import requests
import uuid
from datetime import datetime
import json

class Bill(Crud, StatusObject):
    def __init__(self, id = None):
        Crud.__init__(self, id, 'bill')
        StatusObject.__init__(self, 2)

    def new(self, client_id, folder_id):
        bill_id = str(uuid.uuid4())
        self.id = f"{client_id}/{folder_id}/{bill_id}"
        return [True, {}, None]

    def edit(self, data):
        data['id'] = self.id
        self.before_delete()
        if not "lang" in data or data["lang"] not in ["fr", "en"]:
            return [False, "Invalid 'lang', 'fr' or 'en' only", 400]
        if not "bill_type" in data or data["bill_type"] not in ["invoice", "provision"]:
          return [False, "Invalid 'type' of bill", 404]
        if not "TVA" in data or not any([isinstance(data["TVA"], x) for x in [float, int]]):
          return [False, "Invalid 'TVA' float or int", 400]
        if not "bank" in data or not isinstance(data["bank"], str):
          return [False, "Invalid 'bank' str", 400]
        if not "before_payment" in data or not isinstance(data["before_payment"], int):
          return [False, "Invalid 'before_payment' int", 400]
        tva = data["TVA"]
        data["TVA"] = float(data["TVA"])
        if data["bill_type"] == "invoice":
            ret = self.__invoice(data)
            if ret[0] is False:
                return ret
            data = ret[1]
        if data["bill_type"] == "provision":
            ret = self.__provision(data)
            if ret[0] is False:
                return ret
            data = ret[1]
        data["status"] = 0
        return self._push(data, replace=True)

    def __provision(self, data):
        if not "prov_amount" in data or not any([isinstance(data["prov_amount"], x) for x in [float, int]]):
            return [False, "Invalid 'prov_amount' float or int", 400]
        prov_amount = data["prov_amount"]
        data["price"] = {
            "HT": self.__HT_price(prov_amount),
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
        data["template"] = {
            "name": f"provision_preview{data['lang']}.html",
            "title": f"preview_{self.id.split('/')[-1]}",
            "variables": {
                "amount_HT": self.__currency_format(data["price"]["HT"]),
                "tva_amount": data["TVA"],
                "amount_TTC": self.__currency_format(data["price"]["total"]),
                "banq": data["banq"],
                "address": data["address"]
            }
        }
        data["url"] = self.__generate_fact(data)
        return [True, data, None]

    def __invoice(self, data):
        folder_id = self.id.rsplit('/', 1)[0]
        folder = Folder(folder_id).get()
        if folder[1] is None:
            return [False, f"Invalid folder id: '{folder_id}'", 404]
        if not "timesheet" in data or not isinstance(data["timesheet"], list) or not all([isinstance(x, str) for x in data['timesheet']]):
            return [False, "Invalid 'timesheet' list", 400]
        bank = Bank(data["bank"]).get()
        if bank[1] is None:
            return [False, f"Invalid bank id: '{folder_id}'", 404]
        timesheets = data["timesheet"]
        if len(timesheets) == 0:
            return [False, "Invalid 'timsheet' list", 400]
        if len(timesheets) != len(set(timesheets)):
            return [False, "Duplicates in 'timesheet' list", 400]
        provision_objects = []
        timesheet_objects = []
        prov = []
        if "provisions" in data and isinstance(data["provisions"], list) and all([isinstance(x, str) for x in data['provisions']]):
            for prov_id in data["provisions"]:
                prov_id = f"{folder_id}/{prov_id}"
                bill_object = Bill(prov_id)
                bill = bill_object.get()
                provision_objects.append(bill_object)
                print(bill[1] is None, bill[1]["bill_type"] != "provision", bill[1]["bill_type"])
                if bill[1] is None or bill[1]["bill_type"] != "provision":
                    return [False, f"Invalid provision id: '{prov_id}'", 404]
                if bill[1]["status"] in [0, 1]:
                    return [False, f"Unpaid provision", 400]
                if bill[1]["status"] == 3:
                    return [False, f"Provision already in a unpaid bill", 400]
                if bill[1]["status"] == 4:
                    return [False, f"Provision already in a paid bill", 400]
                if bill[1]["status"] != 2:
                    return [False, f"Provision error", 500]
                prov.append(
                    {
                        "date": datetime.utcfromtimestamp(bill[1]["date"]).strftime('%d/%m/%Y'),
                        "price": bill[1]["price"]["total"],
                        "provision_id": bill[1]["id"]
                    }
                )
        data["provisions"] = prov
        data["price"] = {"HT": 0.0, "taxes": 0.0, "total": 0.0}
        lines = []
        for t_id in timesheets:
            ret = self.__calc_timesheet(f"{folder_id}/{t_id}", data)
            if ret[0] is False:
                return ret
            lines.append(ret[1]["line"])
            data["price"]["HT"] += ret[1]["line"]["price_HT"]
            timesheet_objects.append(ret[1]["timesheet_object"])
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
        data['lang'] = 'fr'
        data["template"] = {
            "name": f"invoice_preview{data['lang']}.html",
            "title": f"preview_{self.id.split('/')[-1]}",
            "variables": {
                "lines": data["timesheet"],
                "num": "preview",
                "date": datetime.now().strftime("%d/%m/%Y"),
                "name": f"{folder[1]['name']}",

                "timesheet_sum": self.__currency_format(sum(t["price_HT"] for t in data["timesheet"])),
                "fees_percent": data["fees"]["fees"] if "fees" in data else 0,
                "fees_price_ht": self.__currency_format(data["fees"]["price_HT"] if "fees" in data else 0),

                "reduction_amount": 0 if "reduction" not in data else  self.__currency_format(data["reduction"]["fix"]["amount"]) if "fix" in data["reduction"] else data["reduction"]["percentage"]["amount"],
                "reduction_unit": "%" if "reduction" not in data else "CHF" if "fix" in data["reduction"] else "%",
                "reduction_value": self.__currency_format(0.0) if "reduction" not in data else data["reduction"]["fix"]["valueHT"] if "fix" in data["reduction"] else data["reduction"]["percentage"]["valueHT"],

                "tva_amount": data["TVA"],
                "tva_value": self.__currency_format(data["price"]["taxes"]),
                "provision_amount": sum(t["price"] for t in data["provisions"]),
                "provision_value": self.__currency_format(sum(t["price"] for t in data["provisions"])),

                "total_ttc": self.__currency_format(data["price"]["total"] - sum(t["price"] for t in data["provisions"])),
                "bank": {
                    "benef": bank[1]["benef"],
                    "bic": bank[1]["bic"],
                    "clearing": bank[1]["clearing"],
                    "iban": bank[1]["iban"],
                    "name": bank[1]["name"]      
                },
                "before": data["before_payment"],
                "address": data["address"],
                "qr": self.swiss_qr(
                    {
                        "name": bank[1]["benef"]["name"],
                        "line1": f'{bank[1]["benef"]["house_num"]} {bank[1]["benef"]["street"]}',
                        "line2": f'{bank[1]["benef"]["city"]}, {bank[1]["benef"]["pcode"]}, {bank[1]["benef"]["country"]}',
                    }, 
                    {
                        "name": data["address"][0],
                        "line1": data["address"][1],
                        "line2": data["address"][2],
                    }, 
                    data["lang"], 
                    data["price"]["total"] - sum(t["price"] for t in data["provisions"]) , 
                    bank[1]["iban"], 
                    f"invoice/{data['before_payment']}/preview")[1]
            }
        }
        data["url"] = self.__generate_fact(data)
        self.__status_object_set(3, provision_objects)
        self.__status_object_set(1, timesheet_objects)
        return [True, data, None]

    def __status_object_set(self, status, object_list):
        for i in object_list:
            i.set_status(status)
        return None

    def before_delete(self):
        data = self.get()
        if data[0] is True:
          data = data[1]
        if data is None:
          return [True, None, None]
        if "provisions" in data:
            for i in data["provisions"]:
                self.__status_object_set(2, [Bill(i["provision_id"])])
        if "timesheet" in data:
            for i in data["timesheet"]:
                print(i["timesheet_id"])
                self.__status_object_set(0, [Timesheet(i["timesheet_id"])])
        return [True, data, None]

    def status_trigger(self, status):
        ret = self.get()
        if ret[1] is None:
            retun [False, "error", 500]
        data = ret[1]
        if status == 2:
            if "provisions" in data:
                for i in data["provisions"]:
                    self.__status_object_set(4, [Bill(i["provision_id"])])
            if "lines" in data:
                for i in data["lines"]:
                    self.__status_object_set(2, [Timesheet(i["timesheet_id"])])
        if status != 1:
            return [True, {}, None]
        if "template" in data:
            data["template"]["name"] = data["template"]["name"].replace("_preview", "")
            data["template"]["bucket"] = "files"
            data["template"]["variables"]["num"] = "2022-" + str(int(self.red.filter(
               lambda bill: bill["status"] >= 2
            ).count().run()))
            data["template"]["title"] = self.id.rsplit('/', 1)[0] + "/facture_" + data["template"]["variables"]["num"]
            data["url"] = self.__generate_fact(data)
        self._push(data)
        return [True, data, None]

    def __generate_fact(self, data):
        url = "http://template:8080/template/pdf"
        response = requests.request("POST", url, data=json.dumps(data["template"]), headers={'content-type': "application/json"})
        return json.loads(response.text)

    def __currency_format(self, price):
        return f"{price:_.2f}".replace(".00", ".-").replace("_", " ")

    def __HT_price(self, price):
        return float(price)

    def __taxe(self, price, tva):
        return self.__percentage(price, tva)

    def __TTC_price(self, price, tva):
        return price + self.__taxe(price, tva)

    def __fees_price(self, price, tva):
        return self.__taxe(price, tva)

    def __percentage(self, total, percentage):
        return total * percentage / 100

    def __calc_timesheet(self, timsheet_id, data):
        timesheet_object = Timesheet(timsheet_id)
        d = timesheet_object.get()
        if d[1] is None:
            return [False, f"Invalid timesheet id: '{timsheet_id}'", 404]
        if "price" not in d[1] or not any([isinstance(d[1]["price"], x) for x in [int, float]]):
            return [False, f"Invalid price in timesheet: '{timsheet_id}'", 400]
        if d[1]["status"] == 1:
            print(d[1])
            return [False, f"Timesheet '{timsheet_id}' already in a unpaid bill", 400]
        if d[1]["status"] == 2:
            return [False, f"Timesheet already in a paid bill", 400]
        if d[1]["status"] != 0:
            return [False, f"Timesheet error", 500]
        price_HT =  self.__HT_price(d[1]["price"] * d[1]["duration"])
        taxes = self.__taxe(price_HT, data["TVA"])
        user = User(d[1]["user"]).get()[1]
        if user is None:
            user = "/"
        else:
            user = f"{user['last_name']} {user['first_name']}"
        line = {
            "timesheet_id": timsheet_id,
            "price_HT": round(price_HT, 2),
            "priceHT": self.__currency_format(round(price_HT, 2)),
            "taxes": round(taxes, 2),
            "TVA": data["TVA"],
            "price": round(self.__TTC_price(price_HT, data["TVA"]) , 2),
            "activite": d[1]["desc"],
            "username": user,
            "user": d[1]["user"],
            "timestamp": d[1]["date"],
            "duration": d[1]["duration"],
            "time": str(int(d[1]['duration'])) + "h" + str(int(d[1]['duration'] % 1 * 60)),
            "date": datetime.utcfromtimestamp(d[1]["date"]).strftime('%d/%m/%Y'),
            "rate": self.__currency_format(float(d[1]["price"]))
        }
        return [True, {"line": line, "timesheet_object": timesheet_object}, None]

    def __calc__fees(self, data):
        if "fees" in data:
            print(data["fees"])
            if (not isinstance(data["fees"], int) and not isinstance(data["fees"], float)) or float(data["fees"]) <= 0.0:
                return [False, "Invalid fees value, float", 400]
            print(data["price"]["HT"], data["fees"])
            price_HT = self.__fees_price(data["price"]["HT"], data["fees"])
            data["fees"] = {
                "fees": data["fees"],
                "price_HT": round(price_HT, 2),
                "priceHT": self.__currency_format(round(price_HT, 2)),
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
                price = self.__HT_price(data["reduction"]["fix"])
                data["reduction"]["fix"] = {
                    "amount": data["reduction"]["fix"],
                    "valueHT": self.__currency_format(round(price, 2)),
                    "value_HT": round(price, 2)
                }
                data["price"]["HT"] -= price
            elif "percentage" in data["reduction"]:
                if not any([isinstance(data["reduction"]["percentage"], x) for x in [float, int]]):
                    return [False, "Invalid reduction.percentage float", 400]
                price = self.__percentage(data["price"]["HT"], data["reduction"]["percentage"])
                data["reduction"]["percentage"] = {
                    "amount": data["reduction"]["percentage"],
                    "valueHT": self.__currency_format(round(price, 2)),
                    "value_HT": round(price, 2)
                }
                data["price"]["HT"] -= price
        return [True, data, None]
   
    def swiss_qr(self, creditor, debtor, lang, amount, iban, addi):
        url = "http://qr:8080/generate/svg"

        payload = json.dumps({
          "creditor": {
            "name": creditor["name"],
            "line1": creditor["line1"],
            "line2": creditor["line2"],
          },
          "debtor": {
            "name": debtor["name"],
            "line1": debtor["line1"],
            "line2": debtor["line2"],
          },
          "language": lang,
          "currency": "CHF",
          "amount": amount,
          "account": iban,
          "additional_information": addi,
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        svg = json.loads(response.text)["svg"].replace("height='106mm'", "height='135mm'").replace("width='210mm'", "width='269mm'")
        return [True, svg, None]
