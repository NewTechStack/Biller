from .CRUD import Crud
import uuid

class Timesheet(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'timesheet')

    def new(self, client_id, folder_id):
        timesheet_id = str(uuid.uuid4())
        self.id = f"{client_id}/{folder_id}/{timesheet_id}"
        return [True, {}, None]

    def edit(self, data):
        data['id'] = self.id
        return self._push(data)
