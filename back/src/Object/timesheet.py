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
        self._push(input)
        filter_array =  [
            [{}, "id"],
            [{"client": input["client"]}, "client"],
            [{"client_folder": input["client_folder"]}, "client_folder"],
            [{"user": input["user"]}, "user"],
            [{"user": input["user"], "client": input["client"]}, "user/client"],
            [{"user": input["user"], "client": input["client_folder"]}, "user/client_folder"]
            
        ]
        for f in filter_array:
            self.insert_from_chain(input["date"], f[0], f[1])
        return self.get()
        
    
    def insert_from_chain(self, date, actual_filter = {}, following = "id"):
        res = self.red.filter(actual_filter).filter(r.row["id"].ne(self.id)).filter(r.row["date"].ge("date")).min().default(None).run()
        if res is not None:
            self.red.get(self.id).update({"following": {following: {"is_after_id": res["following"][following]["is_before_id"], "is_before_id": res["id"]}}}).run()
            if res["id"] is not None:
                self.red.get(res["id"]).update({"following": {following: {"is_after_id": self.id}}}).run()
            if res["following"][following]["is_after_id"] is not None:
                self.red.get(res["following"][following]["is_after_id"]).update({"following": {following: {"is_before_id": self.id}}}).run()
        else:
            res = self.red.filter(actual_filter).filter(r.row["id"].ne(self.id)).filter(r.row["date"].lt("date")).max().default(None).run()
            if res is not None:
                self.red.get(self.id).update({"following": {following: {"is_after_id": res["id"], "is_before_id": None}}}).run()
            if res["following"][following]["is_after_id"] is not None:
                self.red.get(res["following"][following]["is_after_id"]).update({"following": {following: {"is_before_id": self.id}}}).run()
            if res is None:
                self.red.get(self.id).update({"following": {following: {"is_after_id": None, "is_before_id": None}}}).run()
        res = [{"id": None, "following": {following: {"is_before_id": None, "is_after_id": None}}}]
        
    
    def delete(self):
        if self.id is None:
            return [False, "Invalid id", 404]
        res = dict(self.red.get(self.id).run())
        order = res["order"]
        filter_array =  ["id", "client", "client_folder", "user", "user/client", "user/client_folder"]
        for f in filter_array:
            self.remove_from_chain(self.id, f)
        self.red.get(self.id).delete().run()
        return [True, {'id': self.id}, None]

    def remove_from_chain(self, id, following = "id"):
        res = self.red.get(self.id).run()
        if res is None:
            return
        self.red.get(self.id).update({"following": {following: {"is_after_id": None, "is_before_id": None}}}).run()
        self.red.get(res["following"][following]["is_after_id"]).update({"following": {following: {"is_before_id": res["following"][following]["is_before_id"]}}}).run()
        self.red.get(res["following"][following]["is_before_id"]).update({"following": {following: {"is_after_id": res["following"][following]["is_after_id"]}}}).run()
