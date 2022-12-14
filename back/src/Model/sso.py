from Controller.basic import check
from Object.sso import Sso

def sso_url(cn, nextc):
    err = Sso().get_url()
    return cn.call_next(nextc, err)

def sso_token(cn, nextc):
    err = check.contain(cn.rt, ["conn"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Sso().get_token(cn.rt["conn"])
    return cn.call_next(nextc, err)

def sso_verify_token(cn, nextc):
    err = check.contain(cn.hd, ["usrtoken"], "HEAD")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.private["sso"] = Sso()
    err = cn.private["sso"].verify(cn.hd["usrtoken"])
    return cn.call_next(nextc, err)
