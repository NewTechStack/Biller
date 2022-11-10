from .rethink import get_conn, r
import uuid
import math

class TimesheetV2():
    def __init__(self):
        self.rf = get_conn().db("ged").table("folder")
        self.rt = get_conn().db("ged").table("timesheet")

    def grouped_by_folder(self, page, number, filter):
        if page < 1:
            page = 1
        page -= 1
        if number < 1:
            number = 1
        req = self.rf.filter(filter)
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
        ret = list(req.skip(page * number).limit(number).run())
        for i in ret:
            i["timesheets"] = list(self.rt.filter({"client_folder": {"id": i["id"].split("/")[1]}}).with_fields('id').run())
        return [True, {"list": ret, "pagination": pagination}, None]
