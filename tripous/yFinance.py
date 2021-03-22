#!/usr/bin/env python
# coding: utf-8

# In[4]:


import yfinance as yf
import datetime 
import pandas as pd

def getPlotOfSymbol(tickerSymbol, plotTimeframe = 90, dataTimeframe="max", priceInterval="1d"):
    
    # define plot endtime
    today = datetime.datetime.today()
    # define plot start-stime
    threeMonthsAgo = today - datetime.timedelta(days=plotTimeframe)
    
    #get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)  
    
    try:
        #get the historical prices for this ticker
        tickerDf = tickerData.history(period=dataTimeframe,interval=priceInterval)
    except:
        # for 500, 429 or else
        return "request_failed"
    
    # for 404
    if len(tickerDf) == 0:
        return "not_found"
    
    # if everything went well
    
    ## turn datestrings to datetime
    tickerDf.index = pd.to_datetime(tickerDf.index)
    ## get open prices to get as close to the date as possible
    opPriceDF= tickerDf["Open"]

    # get currency fo the displayed prices
    currency = tickerData.info['currency']
    
    ## plot df to graph
    ax = opPriceDF.plot(figsize=(15,5),
                xlim =[threeMonthsAgo, today],
                ylim =[0,500],
                xlabel="Date",
                ylabel="Price in "+ currency,               
                title='Stock Prices of ' + tickerSymbol)

    ## create individual filename for every request
    timestamp = datetime.datetime.now().timestamp()
    timestamp = str(timestamp).replace(".","-")
    filename = tickerSymbol + "_" + "graph" + "_" + timestamp + '.png'
    
    ## save filename to directory
    ax.figure.savefig(filename)    
    
    ## return filname for display and Dataframe for further processing
    return filename, opPriceDF

