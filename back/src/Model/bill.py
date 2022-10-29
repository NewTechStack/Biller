def bill_get_all(cn, nextc):
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
    err = Bill().get_all(page, number, cn.pr["filter"], cn.pr['exclude'], match=match, greater=greater, less=less)
    return cn.call_next(nextc, err)

def bill_new(cn, nextc):
    client_id = cn.rt["client"]
    folder_id = cn.rt["folder"]
    cn.private['bill'] = Bill()
    err = cn.private['bill'].new(client_id, folder_id)
    return cn.call_next(nextc, err)

def bill_set_by_id(cn, nextc):
    client_id = cn.rt["client"]
    folder_id = cn.rt["folder"]
    bill_id = cn.rt["bill"]
    cn.private['bill'] = Bill(f"{client_id}/{folder_id}/{bill_id}")
    err = [True, {}, None]
    return cn.call_next(nextc, err)

def bill_get(cn, nextc):
    err = cn.private['bill'].get()
    return cn.call_next(nextc, err)

def bill_exist(cn, nextc):
    err = cn.private['bill'].exist()
    return cn.call_next(nextc, err)

def bill_edit(cn, nextc):
    err = cn.private['bill'].edit(cn.pr)
    return cn.call_next(nextc, err)

def bill_delete(cn, nextc):
    err = cn.private['bill'].delete()
    return cn.call_next(nextc, err)
