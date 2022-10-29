from .CRUD import Crud
import uuid

class Bill(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'bill')

    def new(self, client_id, folder_id):
        bill_id = str(uuid.uuid4())
        self.id = f"{client_id}/{folder_id}/{bill_id}"
        return [True, {}, None]

    def edit(self, data):
        data['id'] = self.id
        if not "type" in data or data["type"] not in ["invoice", "provision", "retainer"]:
          return [False, "Invalid 'type'", 404]
        type = data["type"]
        if not "TVA" in data or not isinstance(data["TVA"], bool):
          return [False, "Invalid 'TVA'", 400]
        tva = data["TVA"]
        if not "timesheet" in data or not isinstnace(data["timesheet"], list) or not all([isinstance(x, str) for x in data['timesheet']]):
          return [False, "Invalid 'timesheet' list", 400]
        timesheet = data["timesheet"]
        return self._push(data)
