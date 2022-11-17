from Controller.basic import check
from Object.timesheet import Timesheet
from Object.folder import Folder
from Object.v2 import TimesheetV2

def timesheets_all(cn, nextc):
    page = int(cn.get.get('page', 1))
    number = int(cn.get.get('number', 2)) if 'page' in cn.get else 2
    client_id = cn.get.get('client', None)
    folder_id = cn.get.get('folder', None)
    stime = cn.get.get('stime', None)
    etime = cn.get.get('etime', None)
    err = TimesheetV2().all(page, number, client_id, folder_id, stime, etime)
    return cn.call_next(nextc, err)

def timesheets_by_folder(cn, nextc):
    page = int(cn.get.get('page', 1))
    number = int(cn.get.get('number', 2)) if 'page' in cn.get else 2
    client_id = cn.get.get('client', None)
    folder_id = cn.get.get('folder', None)
    stime = cn.get.get('stime', None)
    etime = cn.get.get('etime', None)
    err = TimesheetV2().grouped_by_folder(page, number, client_id, folder_id, stime, etime)
    return cn.call_next(nextc, err)

def timesheet_get_all(cn, nextc):
    page = int(cn.get.get('page', 1))
    number = int(cn.get.get('number', 2)) if 'page' in cn.get else 2
    match = {'field': 'id', "value": cn.rt["client"] + "/*/"} if 'client' in cn.rt else None
    match = {'field': 'id', "value": "*/" + cn.rt["folder"] + "/" } if 'folder' in cn.rt else match
    match = {'field': 'id', "value": cn.rt["client"]  + "/" + cn.rt["folder"] + "/" } if 'folder' in cn.rt and "client" in cn.rt else match
    greater = None if "greater" not in cn.pr else cn.pr["greater"]
    greater = None if greater is None or "field" not in greater or "value" not in greater else greater
    less = None if "less" not in cn.pr else cn.pr["less"]
    less = None if less is None or "field" not in less or "value" not in less else less
    err = check.contain(cn.pr, ["filter", "exclude"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    if "user_in_charge" in cn.pr["filter"]:
        cn.pr["filter"]["client_folder"] = {}
        cn.pr["filter"]["client_folder"]["id"] = [x["id"].split("/")[1] for x in Folder().get_all(1, 10000000, {"user_in_charge": cn.pr["filter"]["user_in_charge"]}, {}, match=None)[1]["list"]]
        del cn.pr["filter"]["user_in_charge"]
    err = Timesheet().get_all(page, number, cn.pr["filter"], cn.pr['exclude'], match=match, greater=greater, less=less)
    return cn.call_next(nextc, err)

def timesheet_get_all_sum(cn, nextc):
    match = {'field': 'id', "value": cn.rt["client"] + "/*/"} if 'client' in cn.rt else None
    match = {'field': 'id', "value": "*/" + cn.rt["folder"] + "/" } if 'folder' in cn.rt else match
    match = {'field': 'id', "value": cn.rt["client"]  + "/" + cn.rt["folder"] + "/" } if 'folder' in cn.rt and "client" in cn.rt else match
    greater = None if "greater" not in cn.pr else cn.pr["greater"]
    greater = None if greater is None or "field" not in greater or "value" not in greater else greater
    less = None if "less" not in cn.pr else cn.pr["less"]
    less = None if less is None or "field" not in less or "value" not in less else less
    exclude = ["client", "client_folder", "created_at", "created_by", "date", "desc", "id", "lang", "status", "user", "type"]
    err = check.contain(cn.pr, ["filter"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Timesheet().get_all(1, 10000000, cn.pr["filter"], exclude, match=match, greater=greater, less=less)
    if err[0]:
        err = [True, {
                "price": sum([t["duration"] * t["price"] for t in err[1]["list"]]),
                "duration": sum([t["duration"] for t in err[1]["list"]])
               }, None]
    return cn.call_next(nextc, err)

def timesheet_new(cn, nextc):
    client_id = cn.rt["client"]
    folder_id = cn.rt["folder"]
    cn.private['timesheet'] = Timesheet()
    err = cn.private['timesheet'].new(client_id, folder_id)
    return cn.call_next(nextc, err)

def timesheet_set_by_id(cn, nextc):
    client_id = cn.rt["client"]
    folder_id = cn.rt["folder"]
    timesheet_id = cn.rt["timesheet"]
    cn.private['timesheet'] = Timesheet(f"{client_id}/{folder_id}/{timesheet_id}")
    err = [True, {}, None]
    return cn.call_next(nextc, err)

def timesheet_get(cn, nextc):
    err = cn.private['timesheet'].get()
    return cn.call_next(nextc, err)

def timesheet_exist(cn, nextc):
    err = cn.private['timesheet'].exist()
    return cn.call_next(nextc, err)

def timesheet_edit(cn, nextc):
#     cn.pr = check.setnoneopt(cn.pr, ["name", "conterpart", "autrepartie", "associate", "price"])
    err = cn.private['timesheet'].edit(cn.pr)
    return cn.call_next(nextc, err)

def timesheet_delete(cn, nextc):
    err = cn.private['timesheet'].delete()
    return cn.call_next(nextc, err)

def timesheet_status_under_2(cn, nextc):
    err = cn.private['timesheet'].status_under_2()
    return cn.call_next(nextc, err)

def timesheet_change_status(cn, nextc):
    err = check.contain(cn.pr, ["status"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = cn.private['timesheet'].change_status(cn.pr["status"])
    return cn.call_next(nextc, err)
