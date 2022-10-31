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
        if not "type" in data or data["type"] not in ["invoice", "provision", "retainer"]:
          return [False, "Invalid 'type'", 404]
        if not "TVA" in data or not isinstance(data["TVA"], float):
          return [False, "Invalid 'TVA' float", 400]
        tva = data["TVA"]
        data["TVA"] = float(tva)
        if not "TVA_inc" in data or not isinstance(data["TVA"], bool):
          return [False, "Invalid 'TVA_inc' bool", 400]
        data["TVA_inc"] = bool(data["TVA_inc"])
        if data["type"] == "invoice":
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
                price = float(d[1]["price"])
                taxes = price * tva / 100
                price_HT =  price if not data["TVA_inc"] else (price - taxes)
                lines.append({
                    "timesheet_id": t_id,
                    "price_HT": price_HT,
                    "taxes": taxes,
                    "TVA": tva,
                    "price": price_HT + taxes
                })
                data["price"]["HT"] += price_HT
                data["price"]["taxes"] += taxes
                data["price"]["total"] += price_HT + taxes
            data["timesheet"] = lines
        data["url"] = "/docuement/soon"
        data["status"] = 0
        return self._push(data)
