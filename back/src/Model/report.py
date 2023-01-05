from Controller.basic import check
from Object.report import Report

def report_get(cn, nextc):
    err = check.contain(cn.pr, ["start", "end", "user_id"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = Report().get(cn.pr["start"], cn.pr["end"], cn.pr["user_id"])
    return cn.call_next(nextc, err)
