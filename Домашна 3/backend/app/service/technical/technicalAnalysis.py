import pandas as pd
import numpy as np
import talib

from app.service.preparation.preparation import get_stocks_as_dataframe

window = 5
def SMA(data, period=30, column='closing_price'):
    return data[column].rolling(window=period).mean()
def EMA(data, window, column='closing_price'):
    return data[column].ewm(span=window, adjust=False).mean()

def WMA(data, window, column='closing_price'):
    weights = np.arange(1, window + 1)
    return data[column].rolling(window=window).apply(lambda prices:
                                                     np.dot(prices, weights) / weights.sum(),
                                                     raw=True)
def HMA(data, window, column='closing_price'):
    half_length = window // 2
    sqrt_length = int(window ** 0.5)
    wma_half = WMA(data, half_length, column=column)
    wma_full = WMA(data, window, column=column)
    diff = 2 * wma_half - wma_full
    return WMA(pd.DataFrame({column: diff}), sqrt_length, column=column)

def VWMA(data, window):
    price = data['closing_price']
    volume = data['volume']
    return (
            (price * volume).rolling(window=window).sum() /
            volume.rolling(window=window).sum()
    )

def compute_technical_indicators(data):
    # Moving Averages
    periods = [1, 7, 30, 60]
    for period in periods:
        data[f'SMA-{period}'] = SMA(data, period)
        data[f'EMA-{period}'] = EMA(data, period)
        data[f'WMA-{period}'] = WMA(data, period)
        data[f'HMA-{period}'] = HMA(data, period)
        data[f'VWMA-{period}'] = VWMA(data, period)

    # Oscillators
    data['RSI-1'] = talib.RSI(data['closing_price'], timeperiod=2)
    data['RSI-7'] = talib.RSI(data['closing_price'], timeperiod=7)
    data['RSI-30'] = talib.RSI(data['closing_price'], timeperiod=30)

    data[f'MACD-1'], data[f'Signal_1'], _ = talib.MACD(
        data['closing_price'], fastperiod=5, slowperiod=12, signalperiod=9
    )
    data[f'MACD-7'], data[f'Signal_7'], _ = talib.MACD(
        data['closing_price'], fastperiod=12, slowperiod=26, signalperiod=9
    )
    data[f'MACD-30'], data[f'Signal_30'], _ = talib.MACD(
        data['closing_price'], fastperiod=26, slowperiod=50, signalperiod=9
    )

    data['CCI-1'] = talib.CCI(data['max_price'], data['min_price'], data['closing_price'], timeperiod=2)
    data['CCI-7'] = talib.CCI(data['max_price'], data['min_price'], data['closing_price'], timeperiod=7)
    data['CCI-30'] = talib.CCI(data['max_price'], data['min_price'], data['closing_price'], timeperiod=30)

    data['Stochastic-%K-1'], _ = talib.STOCHF(
        data['max_price'], data['min_price'], data['closing_price'], fastk_period=1
    )
    data['Stochastic-%K-7'], _ = talib.STOCHF(
        data['max_price'], data['min_price'], data['closing_price'], fastk_period=7
    )
    data['Stochastic-%K-30'], _ = talib.STOCHF(
        data['max_price'], data['min_price'], data['closing_price'], fastk_period=30
    )

    data['Momentum-1'] = talib.MOM(data['closing_price'], timeperiod=1)
    data['Momentum-7'] = talib.MOM(data['closing_price'], timeperiod=7)
    data['Momentum-30'] = talib.MOM(data['closing_price'], timeperiod=30)

    return data

def generate_moving_average_signals(data):
    # Simple Moving Average Signals
    data['SignalSMA1'] = np.where(data['SMA-1'] > data['SMA-7'], 1, 0)
    data['SignalSMA7'] = np.where(data['SMA-7'] > data['SMA-30'], 1, 0)
    data['SignalSMA30'] = np.where(data['SMA-30'] > data['SMA-60'], 1, 0)

    # Exponential Moving Average Signals
    data['SignalEMA1'] = np.where(data['EMA-1'] > data['EMA-7'], 1, 0)
    data['SignalEMA7'] = np.where(data['EMA-7'] > data['EMA-30'], 1, 0)
    data['SignalEMA30'] = np.where(data['EMA-30'] > data['EMA-60'], 1, 0)

    # Weighted Moving Average Signals
    data['SignalWMA1'] = np.where(data['WMA-1'] > data['WMA-7'], 1, 0)
    data['SignalWMA7'] = np.where(data['WMA-7'] > data['WMA-30'], 1, 0)
    data['SignalWMA30'] = np.where(data['WMA-30'] > data['WMA-60'], 1, 0)

    # Hull Moving Average Signals
    data['SignalHMA1'] = np.where(data['HMA-1'] > data['HMA-7'], 1, 0)
    data['SignalHMA7'] = np.where(data['HMA-7'] > data['HMA-30'], 1, 0)
    data['SignalHMA30'] = np.where(data['HMA-30'] > data['HMA-60'], 1, 0)

    # Volume Weighted Moving Average Signals
    data['SignalVWMA1'] = np.where(data['VWMA-1'] > data['VWMA-7'], 1, 0)
    data['SignalVWMA7'] = np.where(data['VWMA-7'] > data['VWMA-30'], 1, 0)
    data['SignalVWMA30'] = np.where(data['VWMA-30'] > data['VWMA-60'], 1, 0)


def generate_oscillator_signals(data, timeframe):
    suffix = str(timeframe)

    # RSI Signal
    data[f'RSI-Signal-{suffix}'] = np.where(
        data[f'RSI-{timeframe}'] > 70, -1,
        np.where(data[f'RSI-{timeframe}'] < 30, 1, 0)
    )

    # MACD Signal
    data[f'MACD-Signal-{suffix}'] = np.where(
        data[f'MACD-{timeframe}'] > data[f'Signal_{timeframe}'], 1, -1
    )

    # CCI Signal
    data[f'CCI-Signal-{suffix}'] = np.where(
        data[f'CCI-{timeframe}'] > 100, -1,
        np.where(data[f'CCI-{timeframe}'] < -100, 1, 0)
    )

    # Stochastic Signal
    data[f'Stochastic-Signal-{suffix}'] = np.where(
        data[f'Stochastic-%K-{timeframe}'] > 80, -1,
        np.where(data[f'Stochastic-%K-{timeframe}'] < 20, 1, 0)
    )

    # Momentum Signal
    data[f'Momentum-Signal-{suffix}'] = np.where(
        data[f'Momentum-{timeframe}'] > 0, 1, -1
    )

    return data

def aggregate_signals_for_decision(data, timeframe):
    suffix = str(timeframe)
    data[f'MA-Signal-{suffix}'] = (
            data[f'SignalSMA{timeframe}'] +
            data[f'SignalEMA{timeframe}'] +
            data[f'SignalWMA{timeframe}'] +
            data[f'SignalHMA{timeframe}'] +
            data[f'SignalVWMA{timeframe}']
    )

    MA_weight = 1
    RSI_weight = 1.5
    MACD_weight = 1.2
    CCI_weight = 0.8
    Stochastic_weight = 1.0
    Momentum_weight = 1.0

    data[f'CombinedSignal-{suffix}'] = (
            MA_weight * data[f'MA-Signal-{suffix}'] +
            RSI_weight * data[f'RSI-Signal-{suffix}'] +
            MACD_weight * data[f'MACD-Signal-{suffix}'] +
            CCI_weight * data[f'CCI-Signal-{suffix}'] +
            Stochastic_weight * data[f'Stochastic-Signal-{suffix}'] +
            Momentum_weight * data[f'Momentum-Signal-{suffix}']
    )

    threshold = 4
    data[f'FinalDecision-{suffix}'] = np.where(
        data[f'CombinedSignal-{suffix}'] > threshold, 'Buy',
        np.where(data[f'CombinedSignal-{suffix}'] < -threshold, 'Sell', 'Hold')
    )

def perform_technical_analysis(company, period):
    try:
        data = get_stocks_as_dataframe(company)

        if len(data) < 60:
            return "Error: Not enough data"

        compute_technical_indicators(data)
        generate_moving_average_signals(data)
        generate_oscillator_signals(data, period)
        aggregate_signals_for_decision(data, period)

        last_decisions = data[f'FinalDecision-{period}'].tail(period)
        buy_count = (last_decisions == 'Buy').sum()
        sell_count = (last_decisions == 'Sell').sum()
        hold_count = (last_decisions == 'Hold').sum()

        if buy_count > sell_count:
            return 'Buy'
        elif sell_count > buy_count:
            return 'Sell'
        else:
            return 'Hold'

    except Exception as e:
        return f"Error: {str(e)}"