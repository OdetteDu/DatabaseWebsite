#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the rest
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

###########################################################################################
##########################DO NOT CHANGE ANYTHING ABOVE THIS LINE!##########################
###########################################################################################

######################BEGIN HELPER METHODS######################

# helper method to convert times from database (which will return a string)
# into datetime objects. This will allow you to compare times correctly (using
# ==, !=, <, >, etc.) instead of lexicographically as strings.

# Sample use:
# current_time = string_to_time(sqlitedb.getTime())

def string_to_time(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#
# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# See curr_time's `GET' method for sample usage
#
# WARNING: DO NOT CHANGE THIS METHOD
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)

    return jinja_env.get_template(template_name).render(context)

#####################END HELPER METHODS#####################

urls = ('/currtime', 'curr_time',
		'/selecttime', 'select_time',
		'/search', 'search',
		'/item', 'item',
		'/', 'curr_time'
		)

class curr_time:
	# A simple GET request, to '/currtime'
	#
	# Notice that we pass in `current_time' to our `render_template' call
	# in order to have its value displayed on the web page
	def GET(self):
		current_time = sqlitedb.getTime()
		return render_template('curr_time.html', time = current_time)

class select_time:
	# Aanother GET request, this time to the URL '/selecttime'
	def GET(self):
		return render_template('select_time.html')

	# A POST request
	#
	# You can fetch the parameters passed to the URL
	# by calling `web.input()' for **both** POST requests
	# and GET requests
	def POST(self):
		post_params = web.input()
		MM = post_params['MM']
		dd = post_params['dd']
		yyyy = post_params['yyyy']
		HH = post_params['HH']
		mm = post_params['mm']
		ss = post_params['ss'];
		enter_name = post_params['entername']

		selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
		update_message = '(Time updated to: %s.)' % (selected_time)

		t = sqlitedb.transaction()
		try:
			result = sqlitedb.updateTime(selected_time)
		except Exception as e:
			t.rollback()
			update_message = str(e)
		else:
			t.commit()
		return render_template('select_time.html', message = update_message)

class search:
	def GET(self):
		return render_template('search.html')

	def POST(self):
		post_params = web.input()
		itemID = post_params['itemID']
		category = post_params['category']
		description = post_params['description']
		minPrice = post_params['minPrice']
		maxPrice = post_params['maxPrice']
		status = post_params['status']  

		result = sqlitedb.getItem(itemID, category, description, minPrice, maxPrice, status)
		return render_template('search.html', search_result = result)

class item:
	def GET(self):
		try:
			data = web.input()
			itemID = int(data.itemID)
		except Exception as e:
			return render_template('item.html')
		else:
			auctionResult = sqlitedb.getAuctionDetail(itemID)
			categoryResult = sqlitedb.getItemCategory(itemID)
			categoryString = ''
			for cr in categoryResult:
				categoryString += cr['Category']
				categoryString += ', '
			categoryString = categoryString[:len(categoryString)-2]
			bidResult = sqlitedb.getAuctionBids(itemID)
			winnerString = 'None'
			if bidResult:
				winnerString = bidResult[0]['BidderID']

			return render_template('item.html', items = auctionResult, categories = categoryString, bids = bidResult, winner = winnerString)

	def POST(self):
		post_params = web.input()
		itemID = post_params['itemID']
		userID = post_params['userID']
		price = post_params['price']
		update_message = 'Congradulations %s! You successfully made a bid for item %s for $%s' % (userID, itemID, price)

		t = sqlitedb.transaction()
		try:
			makeBidResult = sqlitedb.bid(itemID, userID, price)
		except Exception as e:
			t.rollback()
			update_message = str(e)
			if update_message == 'foreign key constraint failed':
				update_message = 'The username you entered cannot be recognized by our system. Please try again with a different username.'
			elif update_message == 'columns AuctionID, Time are not unique':
				update_message = 'You cannot make a bid at the same time. Please try again later.'
			elif update_message == 'The Bid Amount is not larger than the previous Amount!':
				update_message = 'You have to bid more than the last bid. Please try again with a higher amount.'
		else:
			t.commit()

		auctionResult = sqlitedb.getAuctionDetail(itemID)
		categoryResult = sqlitedb.getItemCategory(itemID)
		categoryString = ''
		for cr in categoryResult:
			categoryString += cr['Category']
			categoryString += ', '
		categoryString = categoryString[:len(categoryString)-2]
		bidResult = sqlitedb.getAuctionBids(itemID)
		winnerString = 'None'
		if bidResult:
			winnerString = bidResult[0]['BidderID']

		return render_template('item.html', items = auctionResult, categories = categoryString, bids = bidResult, winner = winnerString, message = update_message)

###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()
