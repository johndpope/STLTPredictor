import sys
#import urllib2
import pandas as pd
import pandas_datareader.data as web
import io
import requests
from datetime import datetime as dt

def stock_search(symbol, startDate = ('2005', '1', '1'), endDate = ('2017', '11', '11')):
	if not endDate:
		date = dt.datetime.strptime(startDate, "%y/%m/%d")
		date = date + dt.timedelta(days=7)
		endDate = time.strftime("%y+%m+%d")
	start = dt.datetime(int(startDate[0]), int(startDate[1]), int(startDate[2]))
	end = dt.datetime(int(endDate[0]), int(endDate[1]), int(endDate[2]))
	stockData = web.DataReader(symbol, "yahoo", start, end)
	#print stockData.head(10)
	return stockData


def getOpen(opens , day = 0):
	return opens.iloc[day]
def getClose(closes , day = 0):
	return closes.iloc[day]
def getHigh(highs, day = 0):
	return highs.iloc[day]
def getLow(lows, day = 0):
	return lows.iloc[day]
 
if __name__ == '__main__':
	main()
class CompanyInfo(object):
	def __init__(self, symbol):
		self.symbol = symbol
		self.days = 0
		self.bullishness = 0.0
		self.bearishness = 0.0
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
	def printBulls(self):
		print("BULL DAYS:")
		for i in self.bulls:
			print(i)
	def printBears(self):	
		print("BEAR DAYS:")
		for i in self.bears:
			print(i)
	def printWeeklyResults(self):
		print("WEEKLY BULL:")
		print(self.bullishness)
		print("WEEKLY BEAR:")
		print(self.bearishness)
	def getNormalizedResult(self):#Value between -1.0 and 1.0
		normalizedBull = self.bullishness
		normalizedBear = self.bearishness
		if(normalizedBull> 1.0):
			normalizedBear = normalizedBear/normalizedBull
			normalizedBull = normalizedBull/normalizedBull
		if(normalizedBear< -1.0):
			normalizedBull = normalizedBull/normalizedBear
			normalizedBear = normalizedBear/normalizedBear
		return normalizedBear+normalizedBull
	def getBinaryResult(self):#0 or 1 to indicate bullishness
		if(self.bullishness > abs(self.bearishness)):
			return 1
		return 0
	def getBearBullRatio(self):#normalization to a value between 0 and 1 
		ratio = 1.0
		if(self.bearishness != 0):
			ratio = self.bullishness/(abs(self.bearishness) + self.bullishness)
		elif(self.bullishness == 0):
			ratio = 0.0
		return ratio


def analyzeTrends(symbol, date = '2017-11-11'):
	c = CompanyInfo(symbol)
	stockData = stock_search(symbol, startDate = date.split('-'))
	print(stockData)
	for i in range(0,5):
		dayData = stockData.iloc[i]
		dayOpen = pd.to_numeric(getOpen(dayData, 0)) #opens[i]
		dayClose = pd.to_numeric(getClose(dayData, 4)) #closes[i]
		dayHigh = pd.to_numeric(getHigh(dayData, 1)) #highs[i]
		dayLow = pd.to_numeric(getLow(dayData, 2)) #lows[i]
		priceChange = dayClose - dayOpen
		percentChange = (priceChange/dayOpen)*100.0 
		if (abs(percentChange) < 1.0): #Stock didn't have a big change
			if ((dayHigh - dayClose)/dayOpen > .1):
				#bearish reversal
				if(percentChange < 0.0):
					reversalBias = percentChange 
				else:
					reversalBias = -1.0*percentChange
				weight = abs(percentChange)/(((dayHigh - dayClose)/dayOpen)*100+abs(percentChange))
				c.set_bearishness((((1.0-weight)*(dayHigh - dayClose)/dayOpen) + (weight*reversalBias))*-1.0)
			elif ((dayClose - dayLow)/dayOpen > .1):
				#bullish reversal
				if(percentChange < 0.0):
					reversalBias = -1.0*percentChange 
				else:
					reversalBias = percentChange
				weight = abs(percentChange)/((((dayClose - dayLow)/dayOpen)*100)+abs(percentChange))
				c.set_bullishness(((1.0*weight)*(dayClose - dayLow)/dayOpen) + (weight*reversalBias))
			else:#No reversal pattern
				if(percentChange < 0.0):
					c.set_bearishness(percentChange/100)
				else:
					c.set_bullishness(percentChange/100)
		else:#Significant jump or drop
			if (percentChange > 0.0):
				#bullish candle
				openToHigh = dayHigh - dayOpen
				highToClose = dayHigh - dayClose
				retracement = (openToHigh/highToClose)
				if(abs(retracement - .2352) < .02):
					#1st fibonacci number
					c.set_bullishness((percentChange*1.25)/100.0)
				elif (abs(retracement - .3819) < .02):
					#2nd fibo
					c.set_bullishness((percentChange*1.25)/100.0)
				elif (retracement > .5):
					c.set_bullishness((percentChange*.5)/100.0)
				else:
					c.set_bullishness((percentChange * (1.0 - retracement))/100.0)
			else:
				#bearish candle
				openToLow = dayOpen - dayLow
				lowToClose = dayClose - dayLow
				rally = (openToLow/lowToClose)
				if(percentChange < -50.0):
					#1st fibonacci number
					c.set_bearishness(((percentChange*1.5)/100.0)*-1.0)
				else:
					c.set_bearishness(((percentChange * (1.0 - rally))/100.0)*-1.0)
	return c

def main():
#	fileName = ""
#	try:
#		file = open(fileName, "w")
#	except IOError:
#		print ("There was an error writing to", fileName)
#		sys.exit()
	symbols = []
	#highs = [326.670013, 315.5, 318.230011, 317.420013 ,  316.410004]
	#opens = [325.670013, 313.790009, 310.859985, 316.769989, 313.790009]
	#lows = [313.149994, 304.750000, 308.709991, 311.839996, 311.000000]
	#closes = [315.049988, 308.739990, 317.809998, 312.600006, 315.549988]
	date = input("Enter the date you want to search in:")
	stockSymbol = input("Enter your stock symbol, n to exit:")
	while (stockSymbol != 'n'):
		symbols.append(stockSymbol)
		stockSymbol = input("Enter another symbol, n to exit:")
	for s in symbols:
		companyResults = analyzeTrends(s, date)
		assessment = "Bearish"
		if(companyResults.getBinaryResult()):
			assessment = "Bullish"
		print("Our assessment for " + companyResults.symbol + " for this time period is: " + assessment)
		if(companyResults.bullishness != 0.0):
			companyResults.printBulls()
		else:
			print("There are no days with positive trends.")
		if(companyResults.bearishness != 0.0):	
			companyResults.printBears()
		else:
			print("There are no days with negative trends.")
		companyResults.printWeeklyResults()
		print("The bullish to bearish ratio is " + str(companyResults.getBearBullRatio()))
		print("The overall normalized value for the analysis is: " + str(companyResults.getNormalizedResult()))

