from .CRUD import Crud
from .timesheet import Timesheet
import uuid

class Bill(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'bill')

    def new(self, client_id, folder_id):
        bill_id = str(uuid.uuid4())
        self.id = f"{client_id}/{folder_id}/{bill_id}"
        return [True, {}, None]
    
    def edit_status(self, status):
        if status not in [0, 1, 2, 3, 4]:
            return [False, f"Status '{status}' not in range(0, 4)", 400]
        return self._push({'status': status})

    def edit(self, data):
        data['id'] = self.id
        if not "lang" in data or data["lang"] not in ["fr", "en"]:
            return [False, "Invalid 'lang', 'fr' or 'en' only", 400]
        if not "type" in data or data["type"] not in ["invoice", "provision", "retainer"]:
          return [False, "Invalid 'type' of bill", 404]
        if not "TVA" in data or not isinstance(data["TVA"], float):
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
        data["url"] = "/docuement/soon"
        data["status"] = 0
        return self._push(data)
    
    def __invoice(self, data):
        if not "timesheet" in data or not isinstance(data["timesheet"], list) or not all([isinstance(x, str) for x in data['timesheet']]):
            return [False, "Invalid 'timesheet' list", 400]
        timesheets = data["timesheet"]
        if len(timesheets) == 0:
            return [False, "Invalid 'timsheet' list", 400]
        if len(timesheets) != len(set(timesheets)):
            return [False, "Duplicates in 'timesheet' list", 400]
        base_id = self.id.rsplit('/', 1)[0]
        data["price"] = {
            "HT": 0.0,
            "taxes": 0.0,
            "total": 0.0
        }
        data["price"]["HT"] = 0.00
        lines = []
        for t_id in timesheets:
            t_id = f"{base_id}/{t_id}"
            d = Timesheet(t_id).get()
            if d[1] is None:
                return [False, f"Invalid timesheet id: '{t_id}'", 404]
            if "price" not in d[1] or not any([isinstance(d[1]["price"], x) for x in [int, float]]):
                return [False, f"Invalid price in timesheet: '{t_id}'", 400]
            price_HT =  self.__HT_price(float(d[1]["price"]), data["TVA"], data["TVA_inc"])
            taxes = self.__taxe(price_HT, data["TVA"])
            lines.append({
                "timesheet_id": t_id,
                "price_HT": round(price_HT, 2),
                "taxes": round(taxes, 2),
                "TVA": data["TVA"],
                "price": round(self.__TTC_price(price_HT, data["TVA"]) , 2)
            })
            data["price"]["HT"] += price_HT
        if "fees" in data and isinstance(data["fees"], float) and data["fees"] > 0.0:
            price_HT = data["price"]["HT"] * data["fees"] / 100
            data["fees"] = {
                "fees": data["fees"],
                "price_HT": round(price_HT, 2),
                "taxes": round(data["price"]["HT"] * data["fees"] * data["TVA"] / 10000, 2),
                "TVA": data["TVA"],
                "price": round(data["price"]["HT"] * data["fees"] / 100 + data["price"]["HT"] * data["fees"] * data["TVA"] / 10000, 2)
            }
            data["price"]["HT"] += price_HT
        if "reduction" in data:
            if "fix" in data["reduction"]:
                if not isinstance(data["reduction"]["fix"], float):
                    return [False, "Invalid reduction.fix float", 400]
                taxes = data["reduction"]["fix"] * data["TVA"] / 100
                data["reduction"]["fix"] = {
                    "amount": data["reduction"]["fix"],
                    "value_HT": round(data["reduction"]["fix"], 2)
                }
                if data["TVA_inc"]:
                    data["reduction"]["fix"]["value_HT"] = round(data["reduction"]["fix"]["amount"] / (1+(data["TVA"]/100)), 2)
                data["price"]["HT"] -= data["reduction"]["fix"]["value_HT"]
            if "percentage" in data["reduction"]:
                if not isinstance(data["reduction"]["percentage"], float):
                    return [False, "Invalid reduction.percentage float", 400]
                price = data["price"]["HT"] * data["reduction"]["percentage"] / 100
                data["reduction"]["percentage"] = {
                    "amount": data["reduction"]["percentage"],
                    "value_HT": round(price, 2)
                }
                data["price"]["HT"] -= price
        data["price"]["HT"] = round(data["price"]["HT"], 2)
        data["price"]["taxes"] = round(data["price"]["HT"] * data["TVA"] / 100, 2)
        data["price"]["total"] = data["price"]["HT"] + data["price"]["taxes"]
        data["timesheet"] = lines
        return [True, data, None]
    
    def __HT_price(self, price, tva, tva_incl):
        if tva_incl is True:
            price = price / (1+(tva/100))
        return price
    
    def __taxe(self, price, tva):
        return price * tva / 100
    
    def __TTC_price(self, price, tva):
        return price + self.__taxe(price, tva)
