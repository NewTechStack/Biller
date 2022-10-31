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
        if data["type"] == "invoice":
            if not "timesheet" in data or not isinstance(data["timesheet"], list) or not all([isinstance(x, str) for x in data['timesheet']]):
              return [False, "Invalid 'timesheet' list", 400]
            timesheets = data["timesheet"]
            if len(timesheets) == 0:
                return [False, "Invalid 'timsheet' list", 400]
            if len(timesheets) != len(set(timesheets)):
                return [False, "Duplicates in 'timesheet' list", 400]
            base_id = self.id.rsplit('/', 1)[0]
            data["price"] = {}
            data["price"]["HT"] = 0.00
            for id in timesheets:
                id = f"{base_id}/{id}"
                d = Timesheet(id).get()
                if d[1] is None:
                    return [False, f"Invalid timesheet id: '{id}'", 404]
                if "price" not in d[1] or not any([isinstance(d[1]["price"], x) for x in [int, float]]):
                    return [False, f"Invalid price in timesheet: '{id}'", 400]
                data["price"]["HT"] += float(d[1]["price"])
            data["price"]["taxes"] = HT_price * tva / 100
            data["price"]["total"] = HT_price + taxes
        data["url"] = "/docuement/soon"
        data["status"] = 0
        return self._push(data)
