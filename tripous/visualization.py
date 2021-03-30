#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from django.templatetags.static import static

import datetime 
import pandas as pd
import os

import plotly.graph_objects as go

# find date in list closest to pivot date 
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


def getHTMLFromPlotly(priceDF, tickerInfo, plotTimeframe = 90):
    
    # tell pandas to use plotly for visualization instead of matplot
    pd.options.plotting.backend = "plotly"    
    
    # define plot endtime    
    latest = priceDF.index[-1]
    # define plot start-stime
    plotStart = latest - datetime.timedelta(days=plotTimeframe)    
    
    # get currency fo the displayed prices
    currency = tickerInfo["currency"]
    tickerSymbol = tickerInfo["symbol"]
    longName = tickerInfo["longName"]

    # define maximal price in column
    maxPrice = priceDF['price'].max()
         
                          
    ## plot df to graph
    ax = priceDF.plot(labels=dict(index="Date", value="Price in "+ currency, variable="Stock Data"),
                title='Stock Prices of ' + longName)
    
    # limit graph to fit the timeframe and price range of interest
    ax.update_xaxes(range=[plotStart, latest], row=1, col=1)
    ax.update_yaxes(range=[0,maxPrice+10], row=1, col=1)

    # mark the point where the prediction begins
                                        # now is the day, the prediction begins
    predictionMark = nearest(priceDF.index, datetime.datetime.now())
    ax.add_shape(type='line', x0=predictionMark, x1=predictionMark, y0=0,y1=maxPrice+10,
            line=dict(color='red', width=1))


    ## return graph
    return ax.to_html(full_html = False)
