import uuid
# ported from the appmain Javascript source code,
from datetime import datetime


def generateUUID():
    return str(uuid.uuid4())


def getYearMonthFromDate(date):
    return date.strftime('%Y-%m')


def getYearMonthDateFromDate(date):
    return date.strftime('%Y-%m-%d')


def getAccountCalculationIdentity(entity_id):
    t = "ac/" + entity_id
    return t


def getAccountMonthlyCalculationIdentity(entity_id, date):
    r = "mac/" + getYearMonthFromDate(date) + "/" + entity_id
    return r


def getMonthlyBudgetIdentity(entity_id, date):
    r = "mb/" + getYearMonthFromDate(date) + "/" + entity_id
    return r


def getMonthlyBudgetCalculationIdentity(entity_id, date):
    r = "mbc/" + getYearMonthFromDate(date) + "/" + entity_id
    return r


def getMonthlySubCategoryBudgetIdentity(entity_id, date):
    r = "mcb/" + getYearMonthFromDate(date) + "/" + entity_id
    return r


def getMonthlySubCategoryBudgetCalculationIdentity(entity_id, date):
    r = "mcbc/" + getYearMonthFromDate(date) + "/" + entity_id
    return r


def getSettingIdentity(budget_version_id, t):
    n = budget_version_id + "/" + t
    return n


def getScheduledTransactionTransactionId(entity_id, n):
    r = entity_id + "_" + getYearMonthDateFromDate(n)
    return r


def getScheduledTransactionTransferTransactionId(e, n):
    r = e + "_t_" + getYearMonthDateFromDate(n)
    return r


def getScheduledSubTransactionTransferTransactionId(e, n, r):
    a = e + "_st_" + str(r) + "_" + getYearMonthDateFromDate(n)
    return a


def extractMonthFromMonthlySubCategoryBudgetIdentity(t):
    " mcb/YYYY-MM-DD"
    n = t[4:13] + "-01",
    r = datetime.strptime(t, "YYYY-MM-DD")
    return r


def extractMonthFromMonthlySubCategoryBudgetCalculationIdentity(t):
    " mcbc/YYYY-MM-DD"
    n = t[5:14] + "-01",
    r = datetime.strptime(t, "YYYY-MM-DD")
    return r
