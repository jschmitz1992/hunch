#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import datetime 
import pandas as pd

def getDFOfSymbol(tickerSymbol,  dataTimeframe="max", priceInterval="1d", priceType="Open"):
    

    
    #get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)  
    
    #get the historical prices for this ticker
    tickerDf = tickerData.history(period=dataTimeframe,interval=priceInterval)
  
    
    # assert everything went well
                             # for 404
    assert len(tickerDf) > 0, "not_found"
    
    ## turn datestrings to datetime
    tickerDf.index = pd.to_datetime(tickerDf.index)
    ## get open prices to get as close to the date as possible
    priceDF= tickerDf[priceType]


    
    
    ## return filname for display and Dataframe for further processing
    return priceDF ,tickerData.info

