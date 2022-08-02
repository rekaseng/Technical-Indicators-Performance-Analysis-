#!/usr/bin/env python
# coding: utf-8

# In[209]:


import requests
import pandas as pd
from datetime import datetime

#GET LATEST HISTORICAL DATA FROM CRYPTOCOMPARE API
def get_current_data(from_sym, to_sym, limits, url, aggregate):
    minute_url = 'https://min-api.cryptocompare.com/data/v2/histominute'
    hour_url = 'https://min-api.cryptocompare.com/data/v2/histohour'
    day_url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    if url == 'minute':
        url = minute_url
    elif url == 'hour':
        url = hour_url
    else:
        url = day_url
    
    parameters = {'fsym': from_sym,
                 'tsym': to_sym,
                 'limit': limits,
                 'aggregate': aggregate}
        
    #response comes as json
    response = requests.get(url, params = parameters)
    data= response.json()
    
    return data

def get_current_data2(from_sym, to_sym, limits, url, aggregate, timestamp):
    minute_url = 'https://min-api.cryptocompare.com/data/v2/histominute'
    hour_url = 'https://min-api.cryptocompare.com/data/v2/histohour'
    day_url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    if url == 'minute':
        url = minute_url
    elif url == 'hour':
        url = hour_url
    else:
        url = day_url
    
    parameters = {'fsym': from_sym,
                 'tsym': to_sym,
                 'limit': limits,
                 'aggregate': aggregate,
                 'toTs': timestamp}
        
    #response comes as json
    response = requests.get(url, params = parameters)
    data= response.json()
    
    return data


# In[210]:


minute_eth = pd. DataFrame(get_current_data('ETH','USD', 2000, 'minute', 1))
minute_eth = pd.DataFrame(minute_eth['Data']['Data'])
minute_eth['datetime'] = pd.to_datetime(minute_eth['time'],unit='s')
minute_eth= minute_eth.drop(['volumefrom','conversionType', 'conversionSymbol'], axis=1)


# In[211]:


minute_eth2 = pd. DataFrame(get_current_data2('ETH','USD', 2000, 'minute', 1, minute_eth.time[0]-60))
minute_eth2 = pd.DataFrame(minute_eth2['Data']['Data'])
minute_eth2['datetime'] = pd.to_datetime(minute_eth2['time'],unit='s')
minute_eth2= minute_eth2.drop(['volumefrom','conversionType', 'conversionSymbol'], axis=1)

minute_eth3 = pd. DataFrame(get_current_data2('ETH','USD', 2000, 'minute', 1, minute_eth2.time[0]-60))
minute_eth3 = pd.DataFrame(minute_eth3['Data']['Data'])
minute_eth3['datetime'] = pd.to_datetime(minute_eth3['time'],unit='s')
minute_eth3= minute_eth3.drop(['volumefrom','conversionType', 'conversionSymbol'], axis=1)

minute_eth4 = pd. DataFrame(get_current_data2('ETH','USD', 2000, 'minute', 1, minute_eth3.time[0]-60))
minute_eth4 = pd.DataFrame(minute_eth4['Data']['Data'])
minute_eth4['datetime'] = pd.to_datetime(minute_eth4['time'],unit='s')
minute_eth4= minute_eth4.drop(['volumefrom','conversionType', 'conversionSymbol'], axis=1)

minute_eth5 = pd. DataFrame(get_current_data2('ETH','USD', 2000, 'minute', 1, minute_eth4.time[0]-60))
minute_eth5 = pd.DataFrame(minute_eth5['Data']['Data'])
minute_eth5['datetime'] = pd.to_datetime(minute_eth5['time'],unit='s')
minute_eth5= minute_eth5.drop(['volumefrom','conversionType', 'conversionSymbol'], axis=1)


# In[168]:


minute_eth = minute_eth5.append([minute_eth4, minute_eth3, minute_eth2, minute_eth])
minute_eth


# In[169]:


minute_eth['datetime'] = pd.to_datetime(minute_eth['time'],unit='s')


# In[186]:


minute_eth


# In[187]:


minute_eth2 = minute_eth.drop(['datetime'], axis=1)


# In[188]:


minute_eth2.reset_index(drop=True, inplace=True)
minute_eth2


# In[190]:


position = []
position.append('NaN')
for i in range(len(minute_eth)-1):
    if (minute_eth2.close[i]< minute_eth2.close[i+1]):
        position.append('buy')
    elif (minute_eth2.close[i]> minute_eth2.close[i+1]):
        position.append('sell')
    else:
        position.append('neutral')


# In[191]:


minute_eth2['position']= position


# In[192]:


minute_eth2


# In[193]:


minute_eth2 = minute_eth2.dropna() 


# In[194]:


X = minute_eth2.iloc[:,5:-1]
y = minute_eth2.iloc[:, -1]


# In[195]:


y


# In[55]:


minute_eth.to_csv('minute_eth.csv')


# In[196]:


split = int(len(minute_eth2)*0.8)
X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]


# In[124]:


import ta


# In[125]:


# TA's RSI
minute_eth['rsi'] = ta.momentum.rsi(minute_eth.close, window=14) 
# TA's Stochastic Oscillator
minute_eth['stoch'] = ta.momentum.stoch(minute_eth.high, minute_eth.low, minute_eth.close, window=14, smooth_window=3)
# TA's Commodity Channel Index 
minute_eth['cci'] = ta.trend.cci(minute_eth.high, minute_eth.low, minute_eth.close, window = 20)
# TA's Stochastic RSI
minute_eth['stochrsi'] = ta.momentum.stochrsi(minute_eth.close) 
# TA's Schaff Trend Cycle (STC)
minute_eth['stc'] = ta.trend.stc(minute_eth.close) 
# TA's Williams Percent Range
minute_eth['williams_r'] = ta.momentum.williams_r(minute_eth.high, minute_eth.low,minute_eth.close) 
# TA's Ultimate Oscillator
minute_eth['ultimate_oscillator'] = ta.momentum.ultimate_oscillator(minute_eth.high, minute_eth.low,minute_eth.close) 
# TA's Money Flow Index
minute_eth['mfi'] = ta.volume.money_flow_index(minute_eth.high, minute_eth.low,minute_eth.close,minute_eth.volumeto)
# TA's Bollinger high band
minute_eth['bollinger_high'] = ta.volatility.bollinger_hband_indicator(minute_eth.close)
# TA's Bollinger low band
minute_eth['bollinger_low'] = ta.volatility.bollinger_lband_indicator(minute_eth.close)
# TA's Keltner Channel High Band Indicator (KC)
minute_eth['kc_high'] = ta.volatility.keltner_channel_hband_indicator(minute_eth.high, minute_eth.low,minute_eth.close, window=20, window_atr=10)
# TA's Keltner Channel Low Band Indicator (KC)
minute_eth['kc_low'] = ta.volatility.keltner_channel_lband_indicator(minute_eth.high, minute_eth.low,minute_eth.close, window=20, window_atr=10)


# In[189]:


# TA's RSI
minute_eth2['rsi'] = ta.momentum.rsi(minute_eth2.close, window=14) 
# TA's Stochastic Oscillator
minute_eth2['stoch'] = ta.momentum.stoch(minute_eth2.high, minute_eth2.low, minute_eth2.close, window=14, smooth_window=3)
# TA's Commodity Channel Index 
minute_eth2['cci'] = ta.trend.cci(minute_eth2.high, minute_eth2.low, minute_eth2.close, window = 20)


# In[126]:


import numpy as np

# create a list of RSI conditions
conditions = [
    (minute_eth['rsi'] < 20),
    (minute_eth['rsi'] > 70),
    (minute_eth['rsi'] >= 20) & (minute_eth['rsi'] <= 70)
    ]

# create a list of the values we want to assign for each condition
values = ['buy', 'sell', 'neutral']

# create a new column and use np.select to assign values to it using our lists as arguments
minute_eth['rsisignal'] = np.select(conditions, values)

# STOCHASTIC conditions
conditions = [
    (minute_eth['stoch'] < 20),
    (minute_eth['stoch'] > 80),
    (minute_eth['stoch'] >= 20) & (minute_eth['stoch'] <= 80)
    ]
values = ['buy', 'sell', 'neutral']
minute_eth['stochsignal'] = np.select(conditions, values)


#CCI conditions
conditions = [
    (minute_eth['cci'] < -100),
    (minute_eth['cci'] > 100),
    (minute_eth['cci'] >= -100) & (minute_eth['cci'] <= 100)
    ]
values = ['buy', 'sell', 'neutral']
minute_eth['ccisignal'] = np.select(conditions, values)

#STOCHASTIC RSI conditions
conditions = [
    (minute_eth['stochrsi'] < 0.20),
    (minute_eth['stochrsi'] > 0.80),
    (minute_eth['stochrsi'] >= 0.2) & (minute_eth['stochrsi'] <= 0.8) 
    ]
values = ['buy', 'sell', 'neutral']
minute_eth['stochrsisignal'] = np.select(conditions, values)

#Schaff Trend Cycle (STC) conditions
conditions = [
    (minute_eth['stc'] < 25),
    (minute_eth['stc'] > 75),
    (minute_eth['stc'] >= 25) & (minute_eth['stc'] <= 75) 
    ]
values = ['buy', 'sell', 'neutral']
minute_eth['stcsignal'] = np.select(conditions, values)

#Williams Percent R conditions
conditions = [
    (minute_eth['williams_r'] < -80),
    (minute_eth['williams_r'] > -20),
    (minute_eth['williams_r'] >= -80) & (minute_eth['williams_r'] <= -20) 
    ]
values = ['buy', 'sell', 'neutral']
minute_eth['williams_signal'] = np.select(conditions, values)

#Ultimate Oscillator conditions
conditions = [
    (minute_eth['ultimate_oscillator'] < 30),
    (minute_eth['ultimate_oscillator'] > 70),
    (minute_eth['ultimate_oscillator'] >= 30) & (minute_eth['ultimate_oscillator'] <= 70) 
    ]
values = ['buy', 'sell', 'neutral']
minute_eth['ultimate_signal'] = np.select(conditions, values)

#Money Flow Index conditions
conditions = [
    (minute_eth['mfi'] < 20),
    (minute_eth['mfi'] > 80),
    (minute_eth['mfi'] >= 20) & (minute_eth['mfi'] <= 80) 
    ]
values = ['buy', 'sell', 'neutral']
minute_eth['mfi_signal'] = np.select(conditions, values)

#Bollinger Bands conditions
conditions = [
    (minute_eth['bollinger_high'] == 1),
    (minute_eth['bollinger_low'] == 1),
    (minute_eth['bollinger_high'] == 0) & (minute_eth['bollinger_low'] == 0) 
    ]
values = ['buy', 'sell', 'neutral']
minute_eth['bb_signal'] = np.select(conditions, values)

# Keltner Channel Indicator (KC) conditions
conditions = [
    (minute_eth['kc_high'] == 1),
    (minute_eth['kc_low'] == 1),
    (minute_eth['kc_high'] == 0) & (minute_eth['kc_low'] == 0) 
    ]
values = ['buy', 'sell', 'neutral']
minute_eth['kc_signal'] = np.select(conditions, values)



# In[127]:


# Profit Loss RSI trades
rsiprofit_trades = 0
rsiloss_trades = 0
rsineutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.rsisignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            rsiprofit_trades = rsiprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            rsiloss_trades = rsiloss_trades+1
        else:
            rsineutral_trades = rsineutral_trades+1
            
    if minute_eth.rsisignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            rsiprofit_trades = rsiprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            rsiloss_trades = rsiloss_trades+1
         else:
            rsineutral_trades = rsineutral_trades+1


# In[31]:


# Profit Loss Stochastic Oscillators trades
stochprofit_trades = 0
stochloss_trades = 0
stochneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.stochsignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            stochprofit_trades = stochprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            stochloss_trades = stochloss_trades+1
        else:
            stochneutral_trades = stochneutral_trades+1
            
    if minute_eth.stochsignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            stochprofit_trades = stochprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            stochloss_trades = stochloss_trades+1
         else:
            stochneutral_trades = stochneutral_trades+1


# In[32]:


# Profit Loss CCI trades
cciprofit_trades = 0
cciloss_trades = 0
ccineutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.ccisignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            cciprofit_trades = cciprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            cciloss_trades = cciloss_trades+1
        else:
            ccineutral_trades = ccineutral_trades+1
            
    if minute_eth.ccisignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            cciprofit_trades = cciprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            cciloss_trades = cciloss_trades+1
         else:
            ccineutral_trades = ccineutral_trades+1


# In[33]:


# Profit Loss STOCHASTIC RSI trades
stochrsiprofit_trades = 0
stochrsiloss_trades = 0
stochrsineutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.stochrsisignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            stochrsiprofit_trades = stochrsiprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            stochrsiloss_trades = stochrsiloss_trades+1
        else:
            stochrsineutral_trades = stochrsineutral_trades+1
            
    if minute_eth.stochrsisignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            stochrsiprofit_trades = stochrsiprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            stochrsiloss_trades = stochrsiloss_trades+1
         else:
            stochrsineutral_trades = stochrsineutral_trades+1


# In[34]:


# Profit Loss STC trades
stcprofit_trades = 0
stcloss_trades = 0
stcneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.stcsignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            stcprofit_trades = stcprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            stcloss_trades = stcloss_trades+1
        else:
            stcneutral_trades = stcneutral_trades+1
            
    if minute_eth.stcsignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            stcprofit_trades = stcprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            stcloss_trades = stcloss_trades+1
         else:
            stcneutral_trades = stcneutral_trades+1


# In[35]:


# Profit Loss WILLIAMS PERCENT R trades
williamsprofit_trades = 0
williamsloss_trades = 0
williamsneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.williams_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            williamsprofit_trades = williamsprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            williamsloss_trades = williamsloss_trades+1
        else:
            williamsneutral_trades = williamsneutral_trades+1
            
    if minute_eth.williams_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            williamsprofit_trades = williamsprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            williamsloss_trades = williamsloss_trades+1
         else:
            williamsneutral_trades = williamsneutral_trades+1


# In[36]:


# Profit Loss ULTIMATE OSCILLATOR trades
ultimateprofit_trades = 0
ultimateloss_trades = 0
ultimateneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.ultimate_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            ultimateprofit_trades = ultimateprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            ultimateloss_trades = ultimateloss_trades+1
        else:
            ultimateneutral_trades = ultimateneutral_trades+1
            
    if minute_eth.ultimate_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            ultimateprofit_trades = ultimateprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            ultimateloss_trades = ultimateloss_trades+1
         else:
            ultimateneutral_trades = ultimateneutral_trades+1


# In[37]:


# Profit Loss MONEY FLOW INDEX trades
mfiprofit_trades = 0
mfiloss_trades = 0
mfineutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.mfi_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            mfiprofit_trades = mfiprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            mfiloss_trades = mfiloss_trades+1
        else:
            mfineutral_trades = mfineutral_trades+1
            
    if minute_eth.mfi_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            mfiprofit_trades = mfiprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            mfiloss_trades = mfiloss_trades+1
         else:
            mfineutral_trades = mfineutral_trades+1


# In[38]:


# Profit Loss BOLLINGER BANDS trades
bbprofit_trades = 0
bbloss_trades = 0
bbneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.bb_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            bbprofit_trades = bbprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            bbloss_trades = bbloss_trades+1
        else:
            bbneutral_trades = bbneutral_trades+1
            
    if minute_eth.bb_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            bbprofit_trades = bbprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            bbloss_trades = bbloss_trades+1
         else:
            bbneutral_trades = bbneutral_trades+1


# In[39]:


# Profit Loss KC trades
kcprofit_trades = 0
kcloss_trades = 0
kcneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.kc_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            kcprofit_trades = kcprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            kcloss_trades = kcloss_trades+1
        else:
            kcneutral_trades = kcneutral_trades+1
            
    if minute_eth.kc_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            kcprofit_trades = kcprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            kcloss_trades = kcloss_trades+1
         else:
            kcneutral_trades = kcneutral_trades+1


# In[26]:


# Profit Loss Stochastic Oscillators trades
stochprofit_trades = 0
stochloss_trades = 0
stochneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.stochsignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            stochprofit_trades = stochprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            stochloss_trades = stochloss_trades+1
        else:
            stochneutral_trades = stochneutral_trades+1
            
    if minute_eth.stochsignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            stochprofit_trades = stochprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            stochloss_trades = stochloss_trades+1
         else:
            stochneutral_trades = stochneutral_trades+1


# In[27]:


# Profit Loss CCI trades
cciprofit_trades = 0
cciloss_trades = 0
ccineutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.ccisignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            cciprofit_trades = cciprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            cciloss_trades = cciloss_trades+1
        else:
            ccineutral_trades = ccineutral_trades+1
            
    if minute_eth.ccisignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            cciprofit_trades = cciprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            cciloss_trades = cciloss_trades+1
         else:
            ccineutral_trades = ccineutral_trades+1


# In[29]:


# Profit Loss STOCHASTIC RSI trades
stochrsiprofit_trades = 0
stochrsiloss_trades = 0
stochrsineutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.stochrsisignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+1]:
            stochrsiprofit_trades = stochrsiprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+1]:
            stochrsiloss_trades = stochrsiloss_trades+1
        else:
            stochrsineutral_trades = stochrsineutral_trades+1
            
    if minute_eth.stochrsisignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+1]:
            stochrsiprofit_trades = stochrsiprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+1]:
            stochrsiloss_trades = stochrsiloss_trades+1
         else:
            stochrsineutral_trades = stochrsineutral_trades+1


# In[22]:


# Profit Loss STC trades
stcprofit_trades = 0
stcloss_trades = 0
stcneutral_trades = 0
for i in range(len(minute_eth)-12) :
    if minute_eth.stcsignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+10]:
            stcprofit_trades = stcprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+10]:
            stcloss_trades = stcloss_trades+1
        else:
            stcneutral_trades = stcneutral_trades+1
            
    if minute_eth.stcsignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+10]:
            stcprofit_trades = stcprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+10]:
            stcloss_trades = stcloss_trades+1
         else:
            stcneutral_trades = stcneutral_trades+1


# In[23]:


# Profit Loss WILLIAMS PERCENT R trades
williamsprofit_trades = 0
williamsloss_trades = 0
williamsneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.williams_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+10]:
            williamsprofit_trades = williamsprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+10]:
            williamsloss_trades = williamsloss_trades+1
        else:
            williamsneutral_trades = williamsneutral_trades+1
            
    if minute_eth.williams_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+10]:
            williamsprofit_trades = williamsprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+10]:
            williamsloss_trades = williamsloss_trades+1
         else:
            williamsneutral_trades = williamsneutral_trades+1


# In[24]:


# Profit Loss ULTIMATE OSCILLATOR trades
ultimateprofit_trades = 0
ultimateloss_trades = 0
ultimateneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.ultimate_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+10]:
            ultimateprofit_trades = ultimateprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+10]:
            ultimateloss_trades = ultimateloss_trades+1
        else:
            ultimateneutral_trades = ultimateneutral_trades+1
            
    if minute_eth.ultimate_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+10]:
            ultimateprofit_trades = ultimateprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+10]:
            ultimateloss_trades = ultimateloss_trades+1
         else:
            ultimateneutral_trades = ultimateneutral_trades+1


# In[25]:


# Profit Loss MONEY FLOW INDEX trades
mfiprofit_trades = 0
mfiloss_trades = 0
mfineutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.mfi_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+10]:
            mfiprofit_trades = mfiprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+10]:
            mfiloss_trades = mfiloss_trades+1
        else:
            mfineutral_trades = mfineutral_trades+1
            
    if minute_eth.mfi_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+10]:
            mfiprofit_trades = mfiprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+10]:
            mfiloss_trades = mfiloss_trades+1
         else:
            mfineutral_trades = mfineutral_trades+1


# In[26]:


# Profit Loss BOLLINGER BANDS trades
bbprofit_trades = 0
bbloss_trades = 0
bbneutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.bb_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+10]:
            bbprofit_trades = bbprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+10]:
            bbloss_trades = bbloss_trades+1
        else:
            bbneutral_trades = bbneutral_trades+1
            
    if minute_eth.bb_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+10]:
            bbprofit_trades = bbprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+10]:
            bbloss_trades = bbloss_trades+1
         else:
            bbneutral_trades = bbneutral_trades+1


# In[27]:


# Profit Loss KC trades
kcprofit_trades = 0
kcloss_trades = 0
kcneutral_trades = 0
for i in range(len(minute_eth)-10) :
    if minute_eth.kc_signal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+10]:
            kcprofit_trades = kcprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+10]:
            kcloss_trades = kcloss_trades+1
        else:
            kcneutral_trades = kcneutral_trades+1
            
    if minute_eth.kc_signal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+10]:
            kcprofit_trades = kcprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+10]:
            kcloss_trades = kcloss_trades+1
         else:
            kcneutral_trades = kcneutral_trades+1


# In[28]:


# Profit Loss RSI trades
rsiprofit_trades = 0
rsiloss_trades = 0
rsineutral_trades = 0
for i in range(len(minute_eth)-1) :
    if minute_eth.rsisignal[i] == 'buy':
        if minute_eth.close[i]< minute_eth.close[i+10]:
            rsiprofit_trades = rsiprofit_trades+1
        elif minute_eth.close[i]> minute_eth.close[i+10]:
            rsiloss_trades = rsiloss_trades+1
        else:
            rsineutral_trades = rsineutral_trades+1
            
    if minute_eth.rsisignal[i] == 'sell':
         if minute_eth.close[i] > minute_eth.close[i+10]:
            rsiprofit_trades = rsiprofit_trades+1
         elif minute_eth.close[i]< minute_eth.close[i+10]:
            rsiloss_trades = rsiloss_trades+1
         else:
            rsineutral_trades = rsineutral_trades+1


# In[40]:


minute_eth


# In[46]:


profit_loss = pd.DataFrame({"Technical_indicators":['RSI', 'STOCH', 'CCI', 'STOCHRSI', 'STC', 'WILLIAMS', 'ULTIMATE', 'MFI', 'BB', 'KC'],
                         "Profit_trades":[rsiprofit_trades, stochprofit_trades, cciprofit_trades,stochrsiprofit_trades, stcprofit_trades, williamsprofit_trades,
                                         ultimateprofit_trades, mfiprofit_trades, bbprofit_trades, kcprofit_trades],
                        "Loss_trades":[rsiloss_trades, stochloss_trades, cciloss_trades,stochrsiprofit_trades, stcloss_trades, williamsloss_trades,
                                         ultimateloss_trades, mfiloss_trades, bbloss_trades, kcloss_trades],
                         "Neutral_trades":[rsineutral_trades, stochneutral_trades, ccineutral_trades,stochrsiprofit_trades, stcneutral_trades, williamsneutral_trades,
                                         ultimateneutral_trades, mfineutral_trades, bbneutral_trades, kcneutral_trades]})


# In[47]:


for i in range(len(profit_loss)):
    percentage = profit_loss.Profit_trades[i]/ (profit_loss.Profit_trades[i]+profit_loss.Loss_trades[i])
    print(percentage)
    


# In[48]:


profit_loss10


# In[80]:


profit_loss10['profitability'] = profit_loss10.Profit_trades/ (profit_loss10.Profit_trades+profit_loss10.Loss_trades+profit_loss10.Neutral_trades)


# In[ ]:





# In[236]:


def profitlosscalc(indicators, profit_trades, loss_trades, neutral_trades):
    profit_trades=0
    loss_trades = 0
    neutral_trades = 0
    for i in range(len(minute_eth)-1) :
        if minute_eth.indicators[i] == 'buy':
            if minute_eth.close[i]< minute_eth.close[i+1]:
                profit_trades = profit_trades+1
            elif minute_eth.close[i]> minute_eth.close[i+1]:
                loss_trades = loss_trades+1
            else:
                neutral_trades = neutral_trades+1
            
        if minute_eth.indicators[i] == 'sell':
             if minute_eth.close[i] > minute_eth.close[i+1]:
                profit_trades = profit_trades+1
             elif minute_eth.close[i]< minute_eth.close[i+1]:
                loss_trades = loss_trades+1
             else:
                neutral_trades = neutral_trades+1
            
    return profit_trades, loss_trades, neutral_trades


# In[240]:


stochrsi_profit, stochrsi_loss, stochrsi_neutral = 0
profitlosscalc(stochrsisignal, stochrsi_profit, stochrsi_loss, stochrsi_neutral)


# In[51]:


minute_eth['position']= position


# In[54]:


minute_eth


# In[ ]:




