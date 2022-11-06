from .rethink import get_conn, r
from datetime import datetime
import math

class StatusObject:
    def __init__(self, trigger = None):
        self.status = True
        self.trigger = trigger
    
    def change_status(self, status):
        if status not in [0, 1, 2, 3, 4]:
            return [False, f"Status '{status}' not in range(0, 4)", 400]
        ret = self.get()
        if ret[1] is None:
            retun [False, "error", 500]
        if int(ret[1]["status"]) > status:
            return [False, "Can't revert status", 401]
        if int(ret[1]["status"]) + 1 > status:
            return [False, "Can't skip status", 401]
        if int(ret[1]["status"]) + 1 == status:
            return [False, "No status update", 401]
        if status == self.trigger:
            ret = self.status_trigger(status)
            if not ret[0]:
                return ret
        return self._push({'status': status}) 
    
    def status_trigger(self, status):
        return
    
    def status_under_2(self):
        ret = self.get()
        if ret[1] is None:
            retun [False, "error", 500]
        if "status" not in ret[1] or int(ret[1]["status"]) >= 2:
            return [False, "Operation only available if status >= 2", 400]
        return [True, {}, None]

class Crud:
    def __init__(self, id, table):
        self.id = id
        try:
            self.red = get_conn().db("ged").table(table)
        except:
            self.red = None
        self.status = False

    def get_all(self, page, number, filter = {}, exclude={}, match = None, inside = None, greater = None, less = None):
        if page < 1:
            page = 1
        page -= 1
        if number < 1:
            number = 1
        max = int(self.red.count().run())
        if  max == 0:
            if page > 1:
                return [False, "Invalid pagination", 404]
            ret = []
            pagination = {
                "total": 0,
                "pages": {
                    "min": 1,
                    "max": 1,
                    "per_page": number,
                    "actual_page": page + 1
                }
            }
        else:
            req = self.red.filter(filter)
            if greater is not None:
                req = req.filter(
                    lambda object: object[greater['field']] > (greater['value'])
                )
            if less is not None:
                req = req.filter(
                    lambda object: object[less['field']] < (less['value'])
                )
            if match is not None:
                req = req.filter(
                    lambda object: object[match['field']].match(match['value'])
                )
            if inside is not None:
                req = req.filter(
                    lambda object: object[inside['field']].contains(inside['value'])
                )
            req = req if int(req.has_fields('date').count().run()) == 0 else req.has_fields('date').order_by(r.desc('date'))
            total = int(req.count().run())
            max = math.floor(total / number + 1) if total % number != 0 else int(total/number)
            max = max + 1 if max == 0 else max
            if max < page + 1:
                return [False, "Invalid pagination", 404]
            pagination = {
                "total": total,
                "pages": {
                    "min": 1,
                    "max": max,
                    "per_page": number,
                    "actual_page": page + 1
                }
            }
            ret = list(req.without(exclude).skip(page * number).limit(number).run())
        return [True, {"list": ret, "pagination": pagination}, None]

    def get(self):
        ret = list(self.red.filter({'id': self.id}).run())
        return [True, ret[0] if len(ret) > 0 else None, None]

    def delete(self):
        if self.id is None:
            return [False, "Invalid id", 404]
        ret = self.red.filter({'id': self.id}).delete().run()
        return [True, {'id': self.id}, None]

    def exist(self):
        print(self.id)
        if self.red.get(self.id).run() is None:
            return [False, f"{self.__class__.__name__} '{self.id}' doesn't exist", 404]
        return [True, {}, None]

    def _push(self, data):
        if self.id is None:
            return [False, "Invalid id", 404]
        data['id'] = self.id
        if self.red.get(self.id).run() is None:
            data['created_at'] = r.expr(datetime.now(r.make_timezone('+02:00')))
            data['created_by'] = "test@test.fr"
            if self.status is True:
                data["status"] = 0 
        res = dict(self.red.insert([data], conflict="update").run())
        return self.get()
