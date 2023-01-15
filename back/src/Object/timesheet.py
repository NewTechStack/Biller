from .CRUD import Crud, StatusObject
import uuid
from .rethink import r

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
        id = self._push(input)
    
    def get_before_date(self, date, actual_filter = {}, following = "id"):
        res = self.red.filter(filter).filter({"following": {following: {"is_before_id": None}}}).run()
        while res["date"] > date or res["following"][following]["is_before_id"] is not None:
            res = self.red.get(res["following"][following]["is_before_id"]).run()
        return res["following"][following]
    
    def delete(self):
        if self.id is None:
            return [False, "Invalid id", 404]
        res = dict(self.red.get(self.id).run())
        order = res["order"]
        self.red.filter({"client": res["client"]}).filter(r.row["order"]["client"] > res["order"]["client"]).update({
            "order": {"client": (r.row["order"]["client"] - 1)}
        }).run()
        self.red.filter({"client_folder": res["client_folder"]}).filter(r.row["order"]["client_folder"] > res["order"]["client_folder"]).update({
            "order": {"client_folder": (r.row["order"]["client_folder"] - 1)}
        }).run()
        self.red.filter({"id": res["id"]}).filter(r.row["order"]["id"] > res["order"]["id"]).update({
            "order": {"id": (r.row["order"]["id"] - 1)}
        }).run()
        self.red.filter({"user": res["user"]}).filter(r.row["order"]["user"] > res["order"]["user"]).update({
            "order": {"user": (r.row["order"]["user"] - 1)}
        }).run()
        self.red.filter({"user": res["user"], "client": res["client"]}).filter(r.row["order"]["user/client"] > res["order"]["user/client"]).update({
            "order": {"user/client": (r.row["order"]["user/client"] - 1)}
        }).run()
        self.red.filter({"user": res["user"], "client_folder": res["client_folder"]}).filter(r.row["order"]["user/client_folder"] > res["order"]["user/client_folder"]).update({
            "order": {"user/client_folder": (r.row["order"]["user/client_folder"] - 1)}
        }).run()
        ret = self.red.filter({'id': self.id}).delete().run()
        return [True, {'id': self.id}, None]
