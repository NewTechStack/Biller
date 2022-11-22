from Controller.basic import check
from Object.bank import Bank

def bank_get_all(cn, nextc):
    page = int(cn.get.get('page', 1))
    number = int(cn.get.get('number', 2)) if 'page' in cn.get else 2
    err = check.contain(cn.pr, ["filter", "exclude"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Bank().get_all(page, number, cn.pr["filter"], cn.pr['exclude'])
    return cn.call_next(nextc, err)

def bank_new(cn, nextc):
    cn.private['ged_bank'] = Bank()
    err = cn.private['ged_bank'].new()
    return cn.call_next(nextc, err)

def bank_set_by_id(cn, nextc):
    cn.private['ged_bank'] = Bank(cn.rt['bank'])
    err = [True, {}, None]
    return cn.call_next(nextc, err)

def bank_get(cn, nextc):
    err = cn.private['ged_bank'].get()
    return cn.call_next(nextc, err)

def bank_exist(cn, nextc):
    err = cn.private['ged_bank'].exist()
    return cn.call_next(nextc, err)

def bank_edit(cn, nextc):
    cn.pr = check.setnoneopt(cn.pr, ["internal_name", "name", "benef", "iban", "clearing", "bic"])
    err = cn.private['ged_bank'].edit(cn.pr['internal_name'], cn.pr['name'], cn.pr['benef'], cn.pr['iban'], cn.pr['clearing'], cn.pr['bic'])
    return cn.call_next(nextc, err)

def bank_delete(cn, nextc):
    err = cn.private['ged_bank'].delete()
    return cn.call_next(nextc, err)
