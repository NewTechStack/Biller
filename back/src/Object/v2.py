from .rethink import get_conn, r
import urllib.parse
import uuid
import math
import time

class BillV2():
    def __init__(self):
        self.rt = get_conn().db("ged").table("timesheet")
        self.ru = get_conn().db("ged").table("user")
        self.rb = get_conn().db("ged").table("bill")
        self.rc = get_conn().db("ged").table("client")
        self.rf = get_conn().db("ged").table("folder")
        
    def all(self, page, number, client_id, folder_id, stime, etime, status, user):
        if page < 1:
            page = 1
        page -= 1
        if number < 1:
            number = 1
        req = self.rb
        if user is not None:
            user = urllib.parse.unquote(user)
            req = req.filter(
                {
                    "user": urllib.parse.unquote(user)
                }
            )
        if client_id is not None:
            client_id = urllib.parse.unquote(client_id)
            req = req.filter(
                {
                    "client": urllib.parse.unquote(client_id)
                }
            )
        if folder_id is not None:
            folder_id = urllib.parse.unquote(folder_id)
            req = req.filter(
                {
                    "client_folder": folder_id
                }
            )
        if stime is not None:
            stime = int(stime)
            req = req.filter(
                lambda doc:
                    doc["date"] >= stime
            )
        if etime is not None:
            etime = int(etime)
            req = req.filter(
                lambda doc:
                    doc["date"] <= etime
            )
        if status is not None:
            status = int(status)
            req = req.filter(
               {"status": status}
            )
        req = req.eq_join(
            "client", 
            self.rc
        ).without(
            {"right": {"id": True}}
        ).zip().eq_join(
            "client_folder", self.rf
        ).without(
            {"right": {"id": True}}
        ).zip().pluck(
            ["id", "type", "date", "name_1", "name_2", "lang", "name", "fees", "status", "price", "timesheet", "provisions", "bill_type", "url", "user", "client_folder"]
        )
        total = int(req.count().run())
        req = req.order_by(r.desc('date'))
        bills = list(req.skip(page * number).limit(number).run())
        sum = {
            "HT": 0,
            "taxes": 0,
            "total": 0
        }
        for bill in bills:
            sum["HT"] += bill["price"]["HT"]
            sum["taxes"] += bill["price"]["taxes"]
            sum["total"] += bill["price"]["total"]
            if bill["bill_type"] == "invoice":
                bill_folder = bill["client_folder"]
                bill['provision_available'] = list(self.rb.filter({"bill_type": "provision", "status": 2, "client_folder": bill_folder}).pluck("id", "price", "date", "url").run())
            del bill["client_folder"]
            t = []
            if "timesheet" in bill:
                for timesheet in bill["timesheet"]:
                    timesheet = {
                    "date": timesheet["timestamp"],
                    "desc": timesheet["activite"],
                    "duration": timesheet["duration"],
                    "id": timesheet["timesheet_id"],
                    "price": timesheet["price_HT"] / timesheet["duration"],
                    "sum": timesheet["price"],
                    "user": dict(self.ru.get(timesheet["user"]).pluck(["id", "image", "lang", "first_name", "last_name"]).run())
                    }
                    t.append(timesheet)
                bill["timesheet"] = t
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
        return [True, {"list": bills, "sum": sum, "pagination": pagination}, None]
    
class FolderV2():
    def __init__(self):
        self.rf = get_conn().db("ged").table("folder")
        self.rt = get_conn().db("ged").table("timesheet")
        self.ru = get_conn().db("ged").table("user")
        
    def get_all(self, page, number, search, client_type, email):
        if page < 1:
            page = 1
        page -= 1
        if number < 1:
            number = 1
        req = self.rt
        if email is not None:
            req = req.filter(
                lambda doc:
                    doc['email'].match(email)
            )
        if client_type is not None:
            req = req.filter(
                {
                    "type": client_type
                }
            )
        if search is not None:
            req = req.filter(lambda doc:
                doc['name'].match(search)
            )
            req = req.filter(
                {
                    "client": client_id
                }
            )
        req = req.eq_join("user_in_charge", self.ru).without({"right": {"id": True}}).zip().pluck(["id", "first_name", "last_name", "name", "type", "email"])
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
        return [True, {"list": list(req.skip(page * number).limit(number).run()), "pagination": pagination}, None]

class TimesheetV2():
    def __init__(self):
        self.rf = get_conn().db("ged").table("folder")
        self.rt = get_conn().db("ged").table("timesheet")
        self.ru = get_conn().db("ged").table("user")
        self.rc = get_conn().db("ged").table("client")
    
    def all(self, page, number, client_id, folder_id, stime, etime, status, user):
        extern_stats = {"op": {}, "meta": {"object": "TimesheetV2", "function": "all4", "kwargs": [page, number, client_id, folder_id, stime, etime, status, user]}}
        if page < 1:
            page = 1
        page -= 1
        if number < 1:
            number = 1
        req = self.rt
        following = "id"
        if user is not None:
            user = urllib.parse.unquote(user)
            req = req.filter(
                {
                    "user": urllib.parse.unquote(user)
                }
            )
            following = "user"
        if client_id is not None:
            client_id = urllib.parse.unquote(client_id)
            req = req.filter(
                {
                    "client": urllib.parse.unquote(client_id)
                }
            )
            if following in ["user"]:
                following = "user/client"
            else:
                following = "client"
        if folder_id is not None:
            folder_id = urllib.parse.unquote(folder_id)
            req = req.filter(
                {
                    "client_folder": folder_id
                }
            )
            if following in ["user", "user/client"]:
                following = "user/client_folder"
            else:
                following = "client_folder"
        if status is not None:
            status = int(status)
            req = req.filter(
               {"status": status}
            )
        if stime is not None:
            stime = int(stime)
            req = req.filter(r.row["date"].ge(stime))
        if etime is not None:
            etime = int(etime)
            req = req.filter(r.row["date"].le(etime))
        ts = time.time()
        all_arr = dict(
            req.map(
                lambda row: {"price" : row["price"].mul(row["duration"]), "duration" : row["duration"],  "total": 1}
            ).reduce(
                lambda left, right: {"price" : left["price"].add(right["price"]), "duration" : left["duration"].add(right["duration"]), "total": left["total"].add(right["total"])}
            ).default({"price" : 0, "duration" : 0, "total": 0}).run()
        )
        total = all_arr["total"]
        sum_arr = {
            "duration": all_arr["duration"] ,
            "price": all_arr["price"]
        }
        res = req.max('date').default(None).do(
                lambda startDoc: 
                    r.range(0, page * number - 1).fold(
                        startDoc, lambda doc, i: 
                            r.branch(
                             doc["following"][following]["is_after_id"].eq(None),
                             doc,
                             self.rt.get(doc["following"][following]["is_after_id"])
                        )
                    )
        ).run()
        timesheets = []
        extern_stats["op"]["page"] = (time.time() - ts) / 3
        extern_stats["op"]["sum"] = (time.time() - ts) / 3
        extern_stats["op"]["count"] = (time.time() - ts) / 3
        ts = time.time()
        to_scroll = number - 1 if (page + 1) * number < total else total - (page + 1) * number
        if res is not None:
            timesheets = list(
                self.rt.get(res["id"]).do(
                    lambda startDoc: 
                        r.range(0, to_scroll).fold(
                            [startDoc], lambda doc, i: 
                                r.branch(
                                    doc["following"][following]["is_after_id"].eq(None),
                                    doc,
                                    doc.add([self.rt.get(doc[i]["following"][following]["is_after_id"])])
                                )
                        )
                ).eq_join( 
                    "client_folder", self.rf 
                ).without(
                    {"right": "id"}
                ).zip().eq_join(
                    "user", self.ru
                ).without(
                    {"right": {"id": True, "price": True}}
                ).zip().eq_join(
                    "client", self.rc
                ).without(
                    {"right": "id"}
                ).zip().pluck(
                    ["id", "date", "name", "desc", "user", "price", "status", "type", "duration", "image", "first_name", "last_name", "name_1", "name_2", "lang"]
                ).run()
            )
        extern_stats["op"]["request"] = time.time() - ts
        extern_stats["op"]["setup_request"] = 0
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
        extern_stats["total"] = sum(extern_stats["op"].values())
        self.rt = get_conn().db("ged").table("stats").insert([extern_stats]).run()
        return [True, {"list": timesheets, "sum": sum_arr, "pagination": pagination}, None]

    def grouped_by_folder(self, page, number, client_id, folder_id, stime, etime, status, user):
        if page < 1:
            page = 1
        page -= 1
        if number < 1:
            number = 1
        req = self.rt
        if user is not None:
            user = urllib.parse.unquote(user)
            req = req.filter(
                {
                    "user": urllib.parse.unquote(user)
                }
            )
        if client_id is not None:
            client_id = urllib.parse.unquote(client_id)
            req = req.filter(
                {
                    "client": urllib.parse.unquote(client_id)
                }
            )
        if folder_id is not None:
            folder_id = urllib.parse.unquote(folder_id)
            req = req.filter(
                {
                    "client_folder": folder_id
                }
            )
        if stime is not None:
            stime = int(stime)
            req = req.filter(
                lambda doc:
                    doc["date"] >= stime
            )
        if etime is not None:
            etime = int(etime)
            req = req.filter(
                lambda doc:
                    doc["date"] <= etime
            )
        if status is not None:
            status = int(status)
            req = req.filter(
               {"status": status}
            )
        sum_arr = {
            "price": float(req.sum(lambda ts: ts["price"].mul(ts["duration"])).run()),
            "duration": float(req.sum('duration').run())
        }
        req = req.order_by(r.desc('date'))
        total = int(
            req.eq_join("client_folder", self.rf).group("right").without("right").zip().ungroup().count().run()
        )
        req = req.eq_join(
                "user", 
                self.ru
            ).without(
                {"right": "id"}
            ).zip().pluck(
                ["id", "client_folder", "date", "desc", "duration", "price", "first_name", "last_name", "image"]
            ).eq_join(
                "client_folder", 
                self.rf
            ).group("right").without("right").zip().ungroup().order_by(r.desc('date')).skip(page * number).limit(number).map(
                lambda doc:
                    {
                        "id": doc["group"]["id"],
                        "client": doc["group"]["id"].split('/')[0],
                        "associates": doc["group"]["associate"],
                        "name": doc["group"]["name"],
                        "user_in_charge": { "id": doc["group"]["user_in_charge"], "price": doc["group"]["user_in_charge_price"] },
                        "timesheets": doc["reduction"]
                    }
            )
        max = math.floor(total / number + 1) if total % number != 0 else int(total/number)
        max = max + 1 if max == 0 else max
        if max < page + 1:
            return [False, "Invalid pagination", 404]
        folders = list(req.run())
        for folder in folders:
            folder["sum"] = {
            "duration": 0,
            "price": 0
            }
            for ts in folder["timesheets"]:
                folder["sum"]["duration"] += ts["duration"]
                folder["sum"]["price"] += ts["duration"] * ts["price"]
            folder["client"] = dict(self.rc.get(folder["client"]).pluck(["id", "name_1", "name_2", "type", "lang"]).run())
            folder["user_in_charge"]["details"] = dict(self.ru.get(folder["user_in_charge"]["id"]).pluck(["first_name", "last_name", "image"]).run())
            associates = []
            for associate in folder["associates"]:
                associates.append(
                    {
                        "id": associate["id"],
                        "price": associate["price"],
                        "details": dict(self.ru.get(associate["id"]).pluck(["first_name", "last_name", "image"]).run())
                    }
                )
            folder["associates"] = associates
        pagination = {
            "total": total,
            "pages": {
                "min": 1,
                "max": max,
                "per_page": number,
                "actual_page": page + 1
            }
        }
        return [True, {"list": folders, "sum": sum_arr, "pagination": pagination}, None]
