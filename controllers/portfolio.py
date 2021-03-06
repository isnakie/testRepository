import math
import numpy as np

#@auth.requires_login()
def index():
    form = SQLFORM(db.Portfolio).process()
    rows = db(db.Portfolio).select()


    for row in rows:
        row.update(Current_Price=getPrice(row.Symbol))
        row.update(Previous_Total=int(row.Purchase_Price)*int(row.Quantity))
        row.update(Current_Total=float(row.Current_Price)*int(row.Quantity))
        row.update(Gain_Loss=float(row.Current_Total)-float(row.Previous_Total))


    WatchForm = SQLFORM(db.WatchList).process()
    WatchListRows = db(db.WatchList).select()
    for row in WatchListRows:
        row.update(Current_Price=getPrice(row.Symbol))

    if request.vars.sym:
        session.sym = request.vars.sym
        redirect(URL('index'))
    graphURL = "https://blash.pythonanywhere.com/blash/static/prices/"+str(session.sym)+".html"
    TitleString = str(session.sym)
    if session.sym is None:
        TitleString = "AAPL"

    return locals()

def manage():
    grid = SQLFORM.grid(db.Portfolio)
    return locals()

def show():
    company = db.Portfolio(request.args(0))
    session.sym = company.Symbol
    redirect("http://blash.pythonanywhere.com/stocks")
    return locals()

def delete():
    query = db(db.Portfolio.id == request.args(0)).select().first()
    remove = db(db.Portfolio.id == query).delete()
    if remove:
        redirect("http://blash.pythonanywhere.com/portfolio")
    return locals()

def deleteWatchList():
    query = db(db.WatchList.id == request.args(0)).select().first()
    remove = db(db.WatchList.id == query).delete()
    if remove:
        redirect("http://blash.pythonanywhere.com/portfolio")
    return locals()

# @cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def getPrice(stock):
    stockFile = '/home/blash/web2py/applications/blash/static/prices/'+str(stock)+'.txt'
    date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile, delimiter=',', unpack=True)
    #Perhaps we can get this information from the Graphing.py instead of reading the file over again.
    return closep[-1]
