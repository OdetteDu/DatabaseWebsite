
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "<>"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

Users = {}
CategoryItemPair = {}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
This function will test if the user exist in the table, and checks if the two user have the same information
Return '' if the user exists
Return a string of what should be insert to the UserTable if the user does not exist
"""
def addUser(userID, rating, location, country):
    result = ''

    if userID in Users:
        if cmp(Users[userID], (rating, location, country)) != 0:
            print 'Error: two user with same userID has different information: \n'
            print userID + Users[userID] + '\n'
            print usreID + rating + location + country
    else:
        Users[userID] = rating, location, country
        result += userID + columnSeparator + rating + columnSeparator + location + columnSeparator + country + '\n'

    return result

def addQuotation(s):
    index = s.find('"')
    if index < 0:
        return s
    else:
        return s[:index+1]+'"'+addQuotation(s[index+1:])

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):

    UserTable = ''
    ClassificationTable = ''
    ItemTable = ''
    AuctionTable = ''
    BidTable = ''

    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """

            # User Table: seller
            seller = item['Seller']
            UserTable += addUser(seller['UserID'], seller['Rating'], item['Location'], item['Country'])

            itemName = item['Name']
            itemDescription = ''

            if item['Description'] != None:
				itemDescription = item['Description']
            else:
				itemDescription = ''

            if '"' in itemName or '"' in itemDescription:
                itemName = '"' + addQuotation(itemName) + '"'
                itemDescription = '"' + addQuotation(itemDescription) + '"'

            ItemTable += item['ItemID'] + columnSeparator + itemName + columnSeparator + itemDescription + '\n'

            # Classification Table
            categories = item['Category']
            for category in categories:
				if (category, item['ItemID']) not in CategoryItemPair:
					ClassificationTable += category + columnSeparator + item['ItemID'] + '\n'
					CategoryItemPair[(category, item['ItemID'])] = 1
				else:
					CategoryItemPair[(category, item['ItemID'])] = CategoryItemPair[(category, item['ItemID'])] + 1

            # Auction Table
            AuctionTable += item['ItemID'] + columnSeparator + item['ItemID']
            AuctionTable += columnSeparator + seller['UserID']
            AuctionTable += columnSeparator + transformDttm(item['Started']) 
            AuctionTable += columnSeparator + transformDttm(item['Ends'])

            if 'Buy_Price' in item:
                AuctionTable += columnSeparator + transformDollar(item['Buy_Price'])
            else:
                AuctionTable += columnSeparator + 'NULL'

            AuctionTable += columnSeparator + transformDollar(item['First_Bid'])
            AuctionTable += columnSeparator + transformDollar(item['Currently'])
            AuctionTable += columnSeparator + item['Number_of_Bids'] + '\n'

            # Bid Table
            bids = item['Bids']
            if bids != None:
                for bid in bids:
                    bid = bid['Bid']

                    bidder = bid['Bidder']
                    
                    if 'Location' in bidder:
                        location = bidder['Location']
                    else:
                        location = 'NULL'

                    if 'Country' in bidder:
                        country = bidder['Country']
                    else:
                        country = 'NULL'

                    UserTable += addUser(bidder['UserID'], bidder['Rating'], location, country)

                    BidTable += item['ItemID'] + columnSeparator + bidder['UserID']
                    BidTable += columnSeparator + transformDttm(bid['Time'])
                    BidTable += columnSeparator + transformDollar(bid['Amount'])+'\n'

    return (UserTable, ItemTable, ClassificationTable, AuctionTable, BidTable)

    
            

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    UserTableFile = open('userTable.dat', 'w')
    ItemTableFile = open('itemTable.dat', 'w')
    ClassificationTableFile = open('classificationTable.dat', 'w')
    AuctionTableFile = open('auctionTable.dat','w')
    BidTableFile = open('bidTable.dat','w')

    for f in argv[1:]:
        if isJson(f):
            UserTableFile.seek(0,2)
            ItemTableFile.seek(0,2)
            ClassificationTableFile.seek(0,2)
            AuctionTableFile.seek(0,2)
            BidTableFile.seek(0,2)

            Result = parseJson(f)

            UserTableFile.write(Result[0])
            ItemTableFile.write(Result[1])
            ClassificationTableFile.write(Result[2])
            AuctionTableFile.write(Result[3])
            BidTableFile.write(Result[4])
            print "Success parsing " + f

    UserTableFile.close()
    ItemTableFile.close()
    ClassificationTableFile.close()
    AuctionTableFile.close()
    BidTableFile.close()

if __name__ == '__main__':
    main(sys.argv)
