#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from django.templatetags.static import static

import datetime 
import pandas as pd
import os
import matplotlib.pyplot as plt


def plotOfDF(priceDF, tickerInfo, plotTimeframe=90, refGraphName="", size = (15,5)):
    # kill all current plot insances
    plt.close('all')

    # define plot endtime
    latest = priceDF.index[-1]
    # define plot start-stime
    threeMonthsAgo = latest - datetime.timedelta(days=plotTimeframe)
    
    
    # get currency fo the displayed prices
    currency = tickerInfo["currency"]
    tickerSymbol = tickerInfo["symbol"]
    
    maxPrice = priceDF['price'].max()

    ## plot df to graph
    ax = priceDF.plot(figsize=size,
                xlim =[threeMonthsAgo, latest],
                ylim =[0, maxPrice+20],
                xlabel="Date",
                ylabel="Price in "+ currency,               
                title='Stock Prices of ' + tickerSymbol)

    ## create individual filename for every request
        # check if filename is specified
    if refGraphName == "":
            timestamp = datetime.datetime.now().timestamp()
            timestamp = str(timestamp).replace(".","-")
            filename = tickerSymbol + "_" + "graph" + "_" + timestamp + '.png'
            ## save filename to directory
                                ## UGLY WORKAROUND TO FIND THE APP DIRECTORY
    else:  
        filename = refGraphName[:-4] + "_variant.png"
    
    
    filePath = os.path.join("tripous", "static","tripous","img","graph",filename)

    ax.figure.savefig(filePath)    
    
    ## return filname for display and Dataframe for further processing
    return filename

