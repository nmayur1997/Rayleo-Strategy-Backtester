#!/usr/bin/env python
# coding: utf-8

# In[29]:


import yfinance as yf
import ta
import pandas as pd
import matplotlib.pyplot as plt


# In[128]:


df = yf.download("BTC-USD", start = "2021-01-01")


# In[129]:


df


# In[130]:


def indicators(df):
    df["SMA_200"]= ta.trend.sma_indicator(df.Close, window = 200)
    df["stoch_k"] = ta.momentum.stochrsi_k(df.Close, window = 10)
    df.dropna(inplace =True)


# In[131]:


indicators(df)


# In[132]:


df["Buy"] = (df.Close>df.SMA_200) & (df.stoch_k < 0.05)


# In[133]:


df.head(50)


# In[134]:


buydates , selldates = [], []
buys, sells = [],[]

last_selldate = pd.to_datetime("1900-01-01")

for row in range(len(df)):
    if len(selldates) > 0:
        last_selldate = selldates[-1]
    if df.iloc[row].Buy:
        buyprice = df.iloc[row].Close * 0.97
        k = 1
        while True:
            if buyprice >= df.iloc[row + k].Low:
                buydate = df.iloc[row+k].name
                break
            elif k> 10:
                break
            else:
                k += 1
        if buydate> last_selldate:
            buydates.append(buydate)
            buys.append(buyprice)
            for j in range(1,11):
                if df.iloc[row+k+j].Close > buyprice:
                    sellprice = df.iloc[row+ k+j].Open
                    selldate = df.iloc[row+ k+j].name
                    sells.append(sellprice)
                    selldates.append(selldate)
                    break
                elif j ==10:
                    sellprice = df.iloc[row+ k+j].Open
                    selldate = df.iloc[row+ k+j].name
                    sells.append(sellprice)
                    selldates.append(selldate)
                    
            
        


# In[135]:


buydates


# In[136]:


selldates


# In[137]:


plt.plot(df.Close)
plt.scatter(df.loc[buydates].index, df.loc[buydates].Close, marker ="^", c="g")
plt.scatter(df.loc[selldates].index, df.loc[selldates].Close, marker ="v", c="r")


# In[138]:


buys


# In[139]:


sells


# In[140]:


[(sell-buy)/buy for sell,buy in zip(sells,buys)]


# In[141]:


profits = pd.DataFrame([(sell-buy)/buy for sell,buy in zip(sells,buys)])


# In[142]:


(profits + 1).cumprod()


# In[143]:


(df.Close.pct_change()+1).cumprod()


# In[ ]:





# In[ ]:




