#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from joblib import dump, load

import numpy as np
import pandas as pd
import glob

# 

# In[2]:

## Simple Helper functions
def parseFloatFromFilename(filename):
    
    nameSplits = filename.split("_")
    numberStr = nameSplits[1]
    floatNr = float(numberStr)
    
    return floatNr

def checkForBetterModel(currentRMSE, symbol):
    betterModel = None     
    modelFileList = glob.glob(symbol + "*" + ".model")   
    
    for modelFile in modelFileList:        
        oldRMSE = parseFloatFromFilename(modelFile)
        
        if oldRMSE < currentRMSE:
            # this old RMSE is the best yet
            ## remember the score to look for even better ones
            currentRMSE = oldRMSE
            ### save the model for later use
            betterModel = modelFile
        
    return betterModel, currentRMSE

## Feature Engineering logic

def dfToOrdinal(df):
    df.index=df.index.map(datetime.datetime.toordinal)

    return df

def dfToDate(df):
    df.index=df.index.map(datetime.datetime.fromordinal)
    
    return df

def preprocessDF(df):
    # save ordinal date as x
    ## shape it to be an one dimensional array
    X = df.index.to_numpy()
    X = X.reshape((-1, 1))
    # save stock price as y
    y = df[df.columns[0]].to_numpy()
    
    return X, y

def predictData(X, fittedModel, daysToBePredicted = 90 ):
    # define regressor
    lastDateEntry = X[-1]
    nextDateEntry = int(lastDateEntry) + 1
    new_x = np.arange(start=nextDateEntry, stop=nextDateEntry + daysToBePredicted ).reshape(-1, 1)
    
    # predict y
    new_y = fittedModel.predict(new_x)
    
    return new_x, new_y

# In[4]:


import datetime 

def predictDF(df, stockData):
    
    # set metadata
    tickerSymbol = stockData["symbol"]

    # convert datetime to ordinal
    df = dfToOrdinal(df)

    # prepare datasets
    train_df, test_df = train_test_split(df, test_size=0.2)

    ## Preprocessing
    train_x, train_y = preprocessDF(train_df)
    test_x, test_y = preprocessDF(test_df)
    
    ## Create and fit Models
    model = LinearRegression()
    print("Learning from data...")
    model = model.fit(train_x, train_y)
    print("𝑓(𝐱) = {} + {}𝑥".format(model.intercept_, model.coef_[0]))
    
    # test model
    pred_y = model.predict(test_x)
    rmse =  mean_squared_error(pred_y, test_y, squared=False)

    # evaluate model
    ## Check for better models doesnt work yet
    betterModel, rmse = checkForBetterModel(rmse, tickerSymbol)
    rmse = round(rmse, 2)

    if betterModel == None:
       # save model
        modelFileName = tickerSymbol + "_" + str(rmse) + '_.model'
        dump(model, modelFileName)  
    else:
        # the older models worked better
        model = load(betterModel) 

    # Prediction
    ## define regressor for prediction
                    ### start at max date in table                  
    lastDateEntry = np.max((np.max(train_x), np.max(test_x)))
    nextDateEntry = int(lastDateEntry) + 1
    new_x = np.arange(start=nextDateEntry, stop=nextDateEntry + 90 ).reshape(-1, 1)
    
    ## predict y
    new_y = model.predict(new_x)

    ## merge and format train, test and predicted data for user consumption
    mergedx = np.append(train_x, test_x)
    mergedx = np.append(mergedx, new_x)

    mergedy = np.append(train_y, test_y)
    mergedy = np.append(mergedy, new_y)
    
    # merge data in one dataframe
    predictedDF = pd.DataFrame(data=mergedy,   # values
                              index=mergedx,   # index
                              columns=df.columns)

    # turn ordinals back into dates
    predictedDF = dfToDate(predictedDF)
    # reverse shuffling during train_test_split, by sorting data for presentation
    predictedDF.sort_index(inplace=True)

    return predictedDF, rmse

