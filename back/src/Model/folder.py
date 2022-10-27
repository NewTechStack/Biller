from Controller.basic import check
from Object.folder import Folder

def folder_get_all(cn, nextc):
    page = int(cn.get.get('page', 1))
    number = int(cn.get.get('number', 2)) if 'page' in cn.get else 2
    match = {'field': 'id', "value": cn.rt["client"] + "/"} if 'client' in cn.rt else None
    err = check.contain(cn.pr, ["filter", "exclude"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Folder().get_all(page, number, cn.pr["filter"], cn.pr['exclude'], match=match)
    return cn.call_next(nextc, err)

def folder_get_by_user(cn, nextc):
    page = int(cn.get.get('page', 1))
    number = int(cn.get.get('number', 2)) if 'page' in cn.get else 2
    match = {'field': 'associate', "value": cn.rt["user"] + "/"} if 'user' in cn.rt else None
    err = check.contain(cn.pr, ["filter", "exclude"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Folder().get_all(page, number, cn.pr["filter"], cn.pr['exclude'], match=match)
    return cn.call_next(nextc, err)

def folder_new(cn, nextc):
    client_id = cn.rt["client"].id
    cn.private['folder'] = Folder()
    err = cn.private['folder'].new(client_id)
    return cn.call_next(nextc, err)

def folder_set_by_id(cn, nextc):
    client_id = cn.rt["client"].id
    folder_id = cn.rt["folder"].id
    cn.private['folder'] = Folder(f"{client_id}/{folder_id}")
    err = [True, {}, None]
    return cn.call_next(nextc, err)

def folder_get(cn, nextc):
    err = cn.private['folder'].get()
    return cn.call_next(nextc, err)

def folder_exist(cn, nextc):
    err = cn.private['folder'].exist()
    return cn.call_next(nextc, err)

def folder_edit(cn, nextc):
    cn.pr = check.setnoneopt(cn.pr, ["name", "conterpart", "autrepartie", "associate", "price"])
    err = cn.private['folder'].edit(cn.pr["name"], cn.pr["conterpart"], cn.pr["autrepartie"], cn.pr["associate"], cn.pr["price"])
    return cn.call_next(nextc, err)

def folder_delete(cn, nextc):
    err = cn.private['folder'].delete()
    return cn.call_next(nextc, err)
