# coding=utf-8
import configparser
from nYNAB import nYNAB

cp=configparser.ConfigParser()
cp.read("ynab.conf")
email=cp.get('AUTHENTICATION','email')
password=cp.get('AUTHENTICATION','password')

YNABobject=nYNAB(email,password,reload=True)

# the catalog is where non budget specific things are stored, like users, settings, budget names
print(YNABobject.catalog)

budgettomodify=YNABobject.budgets[0]

