import pandas as pd
import numpy as np
import talib

from app.service.preparation.preparation import get_stocks_as_dataframe

data=get_stocks_as_dataframe('ALK')
window=5
def SMA(data, period=30, column='closing_price'):
    return data[column].rolling(window=period).mean()
def EMA(data, window,column='closing_price'):
    return data[column].ewm(span=window, adjust=False).mean()
def WMA(data, window, column='closing_price'):
    weights = np.arange(1, window + 1)
    return data[column].rolling(window=window).apply(lambda prices:
                                               np.dot(prices,weights) / weights.sum(),
                                               raw=True)
def HMA(data, window, column='closing_price'):
    half_length = window // 2
    sqrt_length = int(window ** 0.5)
    wma_half = WMA(data, half_length,column=column)
    wma_full = WMA(data, window,column=column)
    diff = 2 * wma_half - wma_full
    return WMA(pd.DataFrame({column: diff}), sqrt_length, column=column)
def VWMA(data, window):
    price = data['closing_price']
    volume = data['volume']
    return (
        (price * volume).rolling(window=window).sum() /
        volume.rolling(window=window).sum()
    )
# data['volume'] = data['volume'].str.replace(',', '')
data['closing_price'] = data['closing_price'].astype(int)
#%%
data['SMA-1'] = SMA(data, 1)
data['SMA-7']=SMA(data, 7)
data['SMA-30']=SMA(data, 30)
data['SMA-60']=SMA(data, 60)
data['EMA-1']=EMA(data,1)
data['EMA-7']=EMA(data,7)
data['EMA-30']=EMA(data,30)
data['EMA-60']=EMA(data,60)
data['WMA-1'] = WMA(data, 1)
data['WMA-7']=WMA(data, 7)
data['WMA-30']=WMA(data, 30)
data['WMA-60']=WMA(data, 60)
data['HMA-1']=HMA(data, 1)
data['HMA-7']=HMA(data, 7)
data['HMA-30']=HMA(data, 30)
data['HMA-60']=HMA(data, 60)
data['VWMA-1'] = VWMA(data, 1)
data['VWMA-7']=VWMA(data, 7)
data['VWMA-30']=VWMA(data, 30)
data['VWMA-60']=VWMA(data, 60)
#%%
data['SignalSMA1']=np.where(data['SMA-1'] > data['SMA-7'], 1, 0)
data['SignalSMA7']=np.where(data['SMA-7'] > data['SMA-30'], 1, 0)
data['SignalSMA30']=np.where(data['SMA-30'] > data['SMA-60'], 1, 0)
#%%
data['SignalEMA1']=np.where(data['EMA-1'] > data['EMA-7'], 1, 0)
data['SignalEMA7']=np.where(data['EMA-7'] > data['EMA-30'], 1, 0)
data['SignalEMA30']=np.where(data['EMA-30'] > data['EMA-60'], 1, 0)
#%%
data['SignalWMA1']=np.where(data['WMA-1'] > data['WMA-7'], 1, 0)
data['SignalWMA7']=np.where(data['WMA-7'] > data['WMA-30'], 1, 0)
data['SignalWMA30']=np.where(data['WMA-30'] > data['WMA-60'], 1, 0)
#%%
data['SignalHMA1']=np.where(data['HMA-1'] > data['HMA-7'], 1, 0)
data['SignalHMA7']=np.where(data['HMA-7'] > data['HMA-30'], 1, 0)
data['SignalHMA30']=np.where(data['HMA-30'] > data['HMA-60'], 1, 0)
#%%
data['SignalVWMA1']=np.where(data['VWMA-1'] > data['VWMA-7'], 1, 0)
data['SignalVWMA7']=np.where(data['VWMA-7'] > data['VWMA-30'], 1, 0)
data['SignalVWMA30']=np.where(data['VWMA-30'] > data['VWMA-60'], 1, 0)
#%%
def calculate_indicators(data):
    data['RSI-1']=talib.RSI(data['closing_price'], timeperiod=2)
    data['RSI-7'] = talib.RSI(data['closing_price'], timeperiod=7)
    data['RSI-30'] = talib.RSI(data['closing_price'], timeperiod=30)
    data['MACD-1'], data['Signal_1'] = talib.MACD(
        data['closing_price'], fastperiod=1, slowperiod=3, signalperiod=2)
    data['MACD-7'], data['Signal_7'], _ = talib.MACD(
        data['closing_price'], fastperiod=3, slowperiod=7, signalperiod=3)
    data['MACD-30'], data['Signal_30'], _ = talib.MACD(
        data['closing_price'], fastperiod=12, slowperiod=30, signalperiod=9)
    data['CCI-1'] = talib.CCI(data['max_price'], data['min_price'], data['closing_price'], timeperiod=1)
    data['CCI-7'] = talib.CCI(data['max_price'], data['min_price'], data['closing_price'], timeperiod=7)
    data['CCI-30'] = talib.CCI(data['max_price'], data['min_price'], data['closing_price'], timeperiod=30)
    data['ATR-1'] = talib.ATR(data['max_price'], data['min_price'], data['closing_price'], timeperiod=1)
    data['ATR-7'] = talib.ATR(data['max_price'], data['min_price'], data['closing_price'], timeperiod=7)
    data['ATR-30'] = talib.ATR(data['max_price'], data['min_price'], data['closing_price'], timeperiod=30)
    data['AD'] = talib.AD(data['max_price'], data['min_price'], data['closing_price'], data['volume'])
    return data


def combine_indicators_for_timeframe(data, timeframe):

    suffix = str(timeframe)
    data[f'MA-Signal-{suffix}'] = (
            data[f'SignalSMA{timeframe}'] +
            data[f'SignalEMA{timeframe}'] +
            data[f'SignalWMA{timeframe}'] +
            data[f'SignalHMA{timeframe}'] +
            data[f'SignalVWMA{timeframe}']
    )

    data[f'RSI-Signal-{suffix}'] = np.where(
        data[f'RSI-{timeframe}'] > 70, -1,
        np.where(data[f'RSI-{timeframe}'] < 30, 1, 0)
    )

    data[f'MACD-Signal-{suffix}'] = np.where(
        data[f'MACD-{timeframe}'] > data[f'Signal_{timeframe}'], 1, -1
    )

    data[f'CCI-Signal-{suffix}'] = np.where(
        data[f'CCI-{timeframe}'] > 100, -1,
        np.where(data[f'CCI-{timeframe}'] < -100, 1, 0)
    )

    data['AD-Signal'] = np.where(data['AD'] > 0, 1, -1)

    data[f'ATR-Signal-{suffix}'] = np.where(
        data[f'ATR-{timeframe}'] > data[f'ATR-{timeframe}'].rolling(window=14).mean(), 1, -1
    )

    data[f'CombinedSignal-{suffix}'] = (
            data[f'MA-Signal-{suffix}'] +
            data[f'RSI-Signal-{suffix}'] +
            data[f'MACD-Signal-{suffix}'] +
            data[f'CCI-Signal-{suffix}'] +
            data['AD-Signal'] +
            data[f'ATR-Signal-{suffix}']
    )

    threshold = 7
    data[f'FinalDecision-{suffix}'] = np.where(
        data[f'CombinedSignal-{suffix}'] > threshold, 'Buy',
        np.where(data[f'CombinedSignal-{suffix}'] < -threshold, 'Sell', 'Hold')
    )

    last_decisions = data[f'FinalDecision-{suffix}'].tail(timeframe)
    buy_count = (last_decisions == 'Buy').sum()
    sell_count = (last_decisions == 'Sell').sum()
    hold_count = (last_decisions == 'Hold').sum()

    if buy_count > sell_count:
        final_decision = 'Buy'
    elif sell_count > buy_count:
        final_decision = 'Sell'
    else:
        final_decision = 'Hold'

    return final_decision