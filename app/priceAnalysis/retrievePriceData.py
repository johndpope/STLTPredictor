import sys
#import urllib2
#from yahoo_finance import Share
#from BeautifulSoup import BeautifulSoup as bs
import pandas as pd
import pandas_datareader.data as web
import io
import requests
from datetime import datetime as dt

def stock_search(symbol, startDate = (2005, 1, 1), endDate = (2017, 11, 11)):
	if not endDate:
		date = dt.datetime.strptime(startDate, "%y/%m/%d")
		date = date + dt.timedelta(days=7)
		endDate = time.strftime("%y+%m+%d")
	start = dt(startDate[0], startDate[1], startDate[2])
	end = dt(endDate[0], endDate[1], endDate[2])
	stockData = web.DataReader(symbol, "yahoo", start, end)
	#print stockData.head(10)
	return stockData
 
if __name__ == '__main__':
	sampleData = stock_search('ADBE')
	print (sampleData)
	truncated = stock_search('ADBE', startDate = (2006, 1, 1))
	print(truncated)
	main()
class CompanyInfo(object):
	def __init__(self, symbol):
		self.symbol = symbol
		self.days = 0
		self.bullishness = 0
		self.bearishness = 0
		self.bulls = []
		self.bears = []
	def set_bullishness(self, bullishness):
		self.bulls.append(bullishness)
		self.bullishness += bullishness
	def set_bearishness(self, bearishness):
		self.bears.append(bearishness)
		self.bearishness += bearishness
	def increment_days(self):
		self.days += 1

def main():
	fileName = ""
	try:
		file = open(fileName, "w")
	except IOError:
		print ("There was an error writing to", fileName)
		sys.exit()
	companies = []
	highs = [326.670013, 315.5, 318.230011, 317.420013 ,  316.410004]
	opens = [325.670013, 313.790009, 310.859985, 316.769989, 313.790009]
	lows = [313.149994, 304.750000, 308.709991, 311.839996, 311.000000]
	closes = [315.049988, 308.739990, 317.809998, 312.600006, 315.549988]
	year = input("Enter the year you want to search in:")
	month = input("Enter the month you want to search in:")
	day = input("Enter the day you want to search in:")
	while (stockSymbol != 'n'):
		stockSymbol = input("Enter your stock symbol, n to exit:")
		companies.append(CompanyInfo(stockSymbol))
	i = 0
	for c in companies:
		for i in range(0,5):
			stockData = stock_search(c.symbol)
			dayOpen = opens[i] #getOpen(stockData)
			dayClose = closes[i]#getClose(stockData)
			dayHigh = highs[i]#getHigh(stockData)
			dayLow = lows[i]#getLow(stockData)
			priceChange = dayClose - dayOpen
			percentChange = (priceChange/dayOpen)*100 
			if (abs(percentChange) < 1): #same
				if ((dayHigh - dayClose)/dayOpen > .1):
					#bearish reversal
					if(percentChange < 0):
						reversalTransform = -1*percentChange 
					else:
						reversalTransform = percentChange
					c.set_bearishness((.9*(dayHigh - dayClose)/dayOpen) + (.1*reversalTransform))
				elif ((dayClose - dayLow)/dayOpen > .1):
					#bullish reversal
					if(percentChange < 0):
						reversalTransform = -1*percentChange 
					else:
						reversalTransform = percentChange
					c.set_bearishness((.9*(dayClose - dayLow)/dayOpen) + (.1*reversalTransform))	
			else:
				if (percentChange > 0):
					#bullish candle
					openToHigh = dayHigh - dayOpen
					highToClose = dayHigh - dayClose
					retracement = (openToHigh/highToClose)
					if(abs(retracement - .2352) < .02):
						#1st fibonacci number
						c.set_bullishness(percentChange*1.25)
					elif (abs(retracement - .3819) < .02):
						#2nd fibo
						c.set_bullishness(percentChange*1.25)
					elif (retracement > .5):
						c.set_bullishness(percentChange*.5)
					else:
						c.set_bullishness(percentChange * (1 - retracement))
				else:
					#bearish candle
					openToLow = dayOpen - dayLow
					lowToClose = dayClose - dayLow
					rally = (openToHigh/highToClose)
					if(percentChange < -50):
						#1st fibonacci number
						c.set_bearishness(percentChange*1.5)
					else:
						c.set_bearishness(percentChange * (1 - retracement))

	print("BULL DAYS")
	for i in companies[0].bulls:
		print(i)
	print("BEAR DAYS")
	for i in companies[0].bears:
	    print(i)
	print("WEEKLY BULL")
	print(companies[0].bullishness)
	print("WEEKLY BEAR")
	print(companies[0].bearishness)
#	if (dailyGain):
#		if ():
#			pass
#
#	elif (dailyLoss):
#		pass
#
#	else:

dailyGain = False
dailyLoss = False
	#stockData = Share(stock) Deprecated/causing errors
	#stockData = Share('ADBE')
	#stockData.get_historical(date, date)

#def get_historical_data(name, number_of_days):
#	data = []
#	url = "https://finance.yahoo.com/quote/" + name + "/history/"
#	rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')
#
#	for each_row in rows:
#		divs = each_row.findAll('td')
#		if divs[1].span.text  != 'Dividend': #Ignore this row in the table
			#I'm only interested in 'Open' price; For other values, play with divs[1 - 5]
#			data.append({'Date': divs[0].span.text, 'Open': float(divs[1].span.text.replace(',',''))})

#	return data[:number_of_days]

#Test
#print get_historical_data('amzn', 15)


#print(stockData)