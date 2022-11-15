from .rethink import get_conn, r
import uuid
import math

class TimesheetV2():
    def __init__(self):
        self.rf = get_conn().db("ged").table("folder")
        self.rt = get_conn().db("ged").table("timesheet")
        self.ru = get_conn().db("ged").table("user")

    def grouped_by_folder(self, page, number, client_id, folder_id, stime, etime):
        if page < 1:
            page = 1
        page -= 1
        if number < 1:
            number = 1
        req = self.rf.filter(
                {"client": "193a46bd-10c0-4eec-8390-91b09779ef3f"}
            ).eq_join(
                "user", 
                self.ru
            ).without(
                {"right": "id"}
            ).zip().pluck(
                ["id", "client_folder", "date", "desc", "duration", "price", "first_name", "last_name", "image"]
            ).eq_join(
                "client_folder", 
                self.ru
            ).group("right").without("right").zip().ungroup().map(
                lambda doc:
                    {
                        "id": doc["group"]["id"], 
                        "name": doc["group"]["name"], 
                        "timesheets": doc["reduction"]
                    }
            )
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
        return [True, {"list": ret, "pagination": pagination}, None]
