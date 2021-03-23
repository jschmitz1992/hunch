#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from django.templatetags.static import static

import datetime 
import pandas as pd
import os



def plotOfDF(priceDF, tickerInfo, plotTimeframe=90):
    
    # define plot endtime
    latest = priceDF.index[-1]
    # define plot start-stime
    threeMonthsAgo = latest - datetime.timedelta(days=plotTimeframe)
    
    
    # get currency fo the displayed prices
    currency = tickerInfo["currency"]
    tickerSymbol = tickerInfo["symbol"]
    
    ## plot df to graph
    ax = priceDF.plot(figsize=(15,5),
                xlim =[threeMonthsAgo, latest],
                ylim =[0,500],
                xlabel="Date",
                ylabel="Price in "+ currency,               
                title='Stock Prices of ' + tickerSymbol)

    ## create individual filename for every request
    timestamp = datetime.datetime.now().timestamp()
    timestamp = str(timestamp).replace(".","-")
    filename = tickerSymbol + "_" + "graph" + "_" + timestamp + '.png'
    
    ## save filename to directory
                        ## UGLY WORKAROUND TO FIND THE APP DIRECTORY
    filePath = os.path.join("tripous", "static","tripous","img","graph",filename)

    ax.figure.savefig(filePath)    
    
    ## return filname for display and Dataframe for further processing
    return filename

