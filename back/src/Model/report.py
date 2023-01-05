from Controller.basic import check
from Object.report import Report

def report_get(cn, nextc):
    err = Report().get(cn.pr["start"], cn.pr["end"], cn.pr["user_id"])
    return cn.call_next(nextc, err)
