from Controller.basic import check
from Object.user import User

def user_get_all(cn, nextc):
    page = int(cn.get.get('page', 1))
    number = int(cn.get.get('number', 2)) if 'page' in cn.get else 2
    err = check.contain(cn.pr, ["filter", "exclude"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = User().get_all(page, number, cn.pr["filter"], cn.pr['exclude'])
    return cn.call_next(nextc, err)

def user_set_by_id(cn, nextc):
    cn.private['ged_user'] = User(cn.rt['user'])
    err = [True, {}, None]
    return cn.call_next(nextc, err)

def user_get(cn, nextc):
    err = cn.private['ged_user'].get()
    return cn.call_next(nextc, err)

def user_exist(cn, nextc):
    err = cn.private['ged_user'].exist()
    return cn.call_next(nextc, err)

def user_edit(cn, nextc):
    cn.pr = check.setnoneopt(cn.pr, ["first_name", "last_name", "email", "phone", "image", "price", "index"])
    err = cn.private['ged_user'].edit(cn.pr['first_name'], cn.pr['last_name'], cn.pr['email'], cn.pr['phone'], cn.pr['image'], cn.pr['price'], cn.pr['index'])
    return cn.call_next(nextc, err)

def user_delete(cn, nextc):
    err = cn.private['ged_user'].delete()
    return cn.call_next(nextc, err)
