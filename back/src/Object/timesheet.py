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
        input = {}
        input['id'] = self.id
        input["client"] = self.id.split("/")[0]
        input["client_folder"] = input["client"] + "/" + self.id.split("/")[1]
        input["date"] = data.get("date", None)
        input["duration"] = data.get("duration", None)
        input["user"] = data.get("user", None)
        input["price"] = data.get("price", None)
        if "extra" in data:
            input["extra"] = data["extra"]
        input["status"] = 0
        if "desc" in data:
            input["desc"] = data["desc"]
        input["order"] = {
            "client": int(self.red.filter({"client": input["client"]}).count().run()) ,
            "client_folder": int(self.red.filter({"client_folder": input["client_folder"]}).count().run()) ,
            "id": int(self.red.count().run()) ,
            "user": int(self.red.filter({"user": input["user"]}).count().run()),
            "user/client": int(self.red.filter({"user": input["user"], "client": input["client"]}).count().run()) ,
            "user/client_folder": int(self.red.filter({"user": input["user"], "client_folder": input["client_folder"]}).count().run())
        }
        return self._push(input)
