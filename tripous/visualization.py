#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from django.templatetags.static import static

import datetime 
import pandas as pd
import os
import matplotlib.pyplot as plt


def plotOfDF(priceDF, tickerInfo, plotTimeframe=90, predictionStart= None,refGraphName="", size = (15,5)):
    # kill all current plot insances
    plt.close('all')

    # define plot endtime
    latest = priceDF.index[-1]
    # define plot start-stime
    startDate = latest - datetime.timedelta(days=plotTimeframe)
    
    
    # get currency and other metadata for the displayed prices
    currency = tickerInfo["currency"]
    tickerSymbol = tickerInfo["symbol"]
    longName = tickerInfo["longName"]

    # define maximal price in column
    maxPrice = priceDF.loc[priceDF.index > startDate]["price"].max()


    ## plot df to graph
    ax = priceDF.plot(figsize=size,
                xlim =[startDate, latest],
                ylim =[0, maxPrice + 5],
                xlabel="Date",
                ylabel="Price in "+ currency,               
                title='Stock Prices of ' + longName)

    ## create individual filename for every request
        # check if filename is specified
    if refGraphName == "":
            timestamp = datetime.datetime.now().timestamp()
            timestamp = str(timestamp).replace(".","-")
            filename = tickerSymbol + "_" + "graph" + "_" + timestamp + '.png'
    else:  
        filename = refGraphName[:-4] + "_variant.png"

        
    
    
    ## save filename to directory
                        ## UGLY WORKAROUND TO FIND THE APP DIRECTORY
    filePath = os.path.join("tripous", "static","tripous","img","graph",filename)

    # if it is a prediction please make sure, that we separate the real and the predicted values
    if predictionStart is not None:
        ax.axvline(priceDF.index[plotTimeframe//2*-1], color='r', linestyle='--')  


                                # padding is already taken care of by the web layout
    ax.figure.savefig(filePath,bbox_inches='tight', pad_inches=0)    
    
    ## return filename for display and Dataframe for further processing
    return filename

