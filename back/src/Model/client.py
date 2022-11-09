from Controller.basic import check
from Object.client import Client

def client_get_all(cn, nextc):
    page = int(cn.get.get('page', 1))
    number = int(cn.get.get('number', 20)) if 'page' in cn.get else 20
    err = check.contain(cn.pr, ["filter", "exclude"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Client().get_all(page, number, cn.pr["filter"], cn.pr['exclude'])
    return cn.call_next(nextc, err)

def client_new(cn, nextc):
    cn.private['client'] = Client()
    err = cn.private['client'].new()
    return cn.call_next(nextc, err)

def client_set_by_id(cn, nextc):
    client_id = cn.rt["client"]
    cn.private['client'] = Client(client_id)
    err = [True, {}, None]
    return cn.call_next(nextc, err)

def client_exist(cn, nextc):
    err = cn.private['client'].exist()
    return cn.call_next(nextc, err)

def client_get(cn, nextc):
    err = cn.private['client'].get()
    return cn.call_next(nextc, err)

def client_edit(cn, nextc):
    cn.pr = check.setnoneopt(cn.pr, ["type", "name_1", "name_2", "email", "phone", "adresse", "lang"])
    err = cn.private['client'].edit(cn.pr["type"], cn.pr["name_1"], cn.pr["name_2"], cn.pr["email"], cn.pr["phone"], cn.pr["adresse"], cn.pr['lang'], cn.pr.get("extra", None))
    return cn.call_next(nextc, err)

def client_delete(cn, nextc):
    err = cn.private['client'].delete()
    return cn.call_next(nextc, err)
