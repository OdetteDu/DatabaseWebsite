
import web

db = web.database(dbn='sqlite',
        db='AuctionBase.db' 
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    query_string = 'select currentTime from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0].currentTime 

def getItem(itemID, category, description, minPrice, maxPrice, status):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select distinct a.itemID, i.name, a.sellerID, a.timeStart, a.timeEnd, a.currently, a.buyPrice, '
    query_string += '(t.currentTime < a.timeStart) as notStarted, (t.currentTime >= a.timeStart and t.currentTime < a.timeEnd and (a.buyPrice is null or a.currently < a.buyPrice)) as open, '
    query_string += '((t.currentTime >= a.timeEnd or (a.buyPrice is not null and a.currently >= a.buyPrice))) as closed '
    query_string += 'from Auction as a, Classification as c, Item as i, CurrentTime as t '
    query_string += 'where a.itemID = c.itemID and c.itemID = i.itemID'
    if itemID:
        query_string = appendWhere(query_string, 'a.itemID = $itemID')
    if category:
        query_string = appendWhere(query_string, 'c.category = $category')
    if description:
        query_string = appendWhere(query_string, "i.description like '%"+description+"%'")
    if minPrice:
        query_string = appendWhere(query_string, 'a.currently >= $minPrice')
    if maxPrice:
        query_string = appendWhere(query_string, 'a.currently <= $maxPrice')
    if status:
        if status == 'notStarted':
            query_string = appendWhere(query_string, 't.currentTime < a.timeStart')
        elif status == 'open':
            query_string = appendWhere(query_string, 't.currentTime >= a.timeStart and t.currentTime < a.timeEnd and (a.buyPrice is null or a.currently < a.buyPrice)')
        elif status == 'closed':
            query_string = appendWhere(query_string, '(t.currentTime >= a.timeEnd or (a.buyPrice is not null and a.currently >= a.buyPrice)')
    query_string += ' limit 100'

    result = query(query_string, {'itemID': itemID, 'category':category, 'minPrice':minPrice, 'maxPrice':maxPrice})
    return result

def getAuctionDetail(itemID):
    query_string = 'select i.name, a.itemID, i.description, a.timeStart, a.timeEnd, a.firstBid, a.buyPrice, a.currently, a.sellerID, u.rating, '
    query_string += '(t.currentTime < a.timeStart) as notStarted, (t.currentTime >= a.timeStart and t.currentTime < a.timeEnd and (a.buyPrice is null or a.currently < a.buyPrice)) as open, '
    query_string += '((t.currentTime >= a.timeEnd or (a.buyPrice is not null and a.currently >= a.buyPrice))) as closed '
    query_string += 'from Auction as a, Item as i, AuctionUser as u, CurrentTime as t '
    query_string += 'where a.itemID = i.itemID and a.sellerID = u.userID '
    query_string += 'and a.itemID = $itemID'
    result = query(query_string, {'itemID': itemID})
    return result

def getItemCategory(itemID):
    query_string = 'select c.category '
    query_string += 'from Auction as a, Item as i, Classification as c '
    query_string += 'where a.itemID = i.itemID and i.itemID = c.itemID '
    query_string += 'and a.itemID = $itemID'
    result = query(query_string, {'itemID': itemID})
    return result

def getAuctionBids(auctionID):
    query_string = 'select b.bidderID, b.time, b.amount '
    query_string += 'from Bid as b '
    query_string += 'where b.auctionID = $auctionID '
    query_string += 'order by b.time desc'
    result = query(query_string, {'auctionID': auctionID})
    return result

def appendWhere(query, where):
    query += ' and '
    query += where
    return query

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
def updateTime(time):
    query_string = 'update CurrentTime set currentTime = $time'
    result = db.query(query_string, {'time':time})
    return result

def bid(auctionID, bidderID, amount):
    query_string = 'select currentTime from CurrentTime'
    result = query(query_string)
    time = result[0].currentTime

    query_string = 'insert into Bid values ($auctionID, $bidderID, $time, $amount)'
    result = db.query(query_string, {'auctionID':auctionID, 'bidderID':bidderID, 'time':time, 'amount':amount})
    return result
