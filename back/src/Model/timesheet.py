from Controller.basic import check
from Object.folder import Folder

def timesheet_get_all(cn, nextc):
    page = int(cn.get.get('page', 1))
    number = int(cn.get.get('number', 2)) if 'page' in cn.get else 2
    match = {'field': 'id', "value": cn.rt["client"] + "/*/"} if 'client' in cn.rt else none
    match = {'field': 'id', "value": "*/" + cn.rt["folder"] + "/" } if 'folder' in cn.rt else match
    err = check.contain(cn.pr, ["filter", "exclude"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Folder().get_all(page, number, cn.pr["filter"], cn.pr['exclude'], match=match)
    return cn.call_next(nextc, err)

def timsheet_new(cn, nextc):
    client_id = cn.rt["client"]
    folder_id = cn.rt["folder"]
    cn.private['timesheet'] = Folder()
    err = cn.private['timesheet'].new(client_id, folder_id)
    return cn.call_next(nextc, err)

def timesheet_set_by_id(cn, nextc):
    client_id = cn.rt["client"]
    folder_id = cn.rt["folder"]
    timesheet_id = cn.rt["timesheet"]
    cn.private['timesheet'] = Folder(f"{client_id}/{folder_id}/{timesheet_id}")
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
