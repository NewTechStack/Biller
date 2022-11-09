from .CRUD import Crud, StatusObject
import uuid

class Timesheet(Crud, StatusObject):
    def __init__(self, id = None):
        Crud.__init__(self, id, 'timesheet')
        StatusObject.__init__(self)

    def new(self, client_id, folder_id):
        timesheet_id = str(uuid.uuid4())
        self.id = f"{client_id}/{folder_id}/{timesheet_id}"
        return [True, {}, None]

    def edit(self, data):
        data['id'] = self.id
        if "desc" in data:
            data["desc"] = [line[i:i+30] for i in range(0, len(data["desc"]), 30)]
        return self._push(data)
