#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd


# 

# In[2]:


## Feature Engineering logic
def dfToOrdinal(df):
    df.index=df.index.map(datetime.datetime.toordinal)
    
    return df 


# In[3]:


def dfToDate(df):
    df.index=df.index.map(datetime.datetime.fromordinal)
    
    return df 


# In[4]:


import datetime 

def predictDF(df):
    # convert datetime to ordinal
    df = dfToOrdinal(df)
    
    ## Preprocessing
    X = df.index.to_numpy()
    X = X.reshape((-1, 1))
    
    y = df[df.columns[0]].to_numpy()

    
    ## Create and fit Models
    model = LinearRegression()
    print("Learning from data...")
    model = model.fit(X, y)
    print("𝑓(𝐱) = {} + {}𝑥".format(model.intercept_,model.coef_[0]))
    
    
    ## Prediction
    # define regressor
    lastDateEntry = X[-1]
    nextDateEntry = int(lastDateEntry) + 1
    new_x = np.arange(start=nextDateEntry, stop=nextDateEntry + 90 ).reshape(-1, 1)
    
    # predict y
    new_y = model.predict(new_x)
    
    # merge and format train data and predicted data for user consumption - not Needed
    mergedx = np.append(X,new_x)
    mergedy = np.append(y,new_y)
    
    
    # merge data in one dataframe
    predictedDF = pd.DataFrame(data=mergedy,   # values
                              index=mergedx,   # index
                              columns=df.columns)  
    
     
    
    # turn ordinals back into dates
    predictedDF = dfToDate(predictedDF)
    
    return predictedDF


# 
