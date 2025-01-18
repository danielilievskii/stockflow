import pandas as pd
import numpy as np
import pandas_ta as ta
from stocks.stock_data_loader import load_stocks_as_dataframe

# Constants
MOVING_AVERAGES_PERIODS = [1, 7, 30, 60]
OSCILLATORS_PERIODS = [1, 7, 30]
THRESHOLDS = {
    "RSI": {"overbought": 70, "oversold": 30},
    "CCI": {"overbought": 100, "oversold": -100},
    "Decision": 4,
}
WEIGHTS = {
    "MA": 1,
    "RSI": 1.5,
    "MACD": 1.2,
    "CCI": 0.8,
    "Momentum": 1.0,
}


# Helper functions for Moving Averages
def calculate_moving_average(data, period, method="SMA", column="closing_price"):
    if method == "SMA":
        return data[column].rolling(window=period).mean()
    elif method == "EMA":
        return data[column].ewm(span=period, adjust=False).mean()
    elif method == "WMA":
        weights = np.arange(1, period + 1)
        return data[column].rolling(window=period).apply(
            lambda prices: np.dot(prices, weights) / weights.sum(), raw=True
        )
    elif method == "HMA":
        half_length = period // 2
        sqrt_length = int(period ** 0.5)
        wma_half = calculate_moving_average(data, half_length, method="WMA", column=column)
        wma_full = calculate_moving_average(data, period, method="WMA", column=column)
        diff = 2 * wma_half - wma_full
        return calculate_moving_average(pd.DataFrame({column: diff}), sqrt_length, method="WMA", column=column)
    elif method == "VWMA":
        price = data[column]
        volume = data['volume']
        return (
                (price * volume).rolling(window=period).sum() /
                volume.rolling(window=period).sum()
        )
    else:
        raise ValueError(f"Unknown method: {method}")


# Technical Indicator Calculation
def compute_technical_indicators(data):
    # Moving Averages
    ma_methods = ["SMA", "EMA", "WMA", "HMA", "VWMA"]
    for method in ma_methods:
        for period in MOVING_AVERAGES_PERIODS:
            data[f'{method}-{period}'] = calculate_moving_average(data, period, method=method)

    # Oscillators
    for period in OSCILLATORS_PERIODS:
        data[f'RSI-{period}'] = ta.rsi(data['closing_price'], length=max(2, period))
        data[f'CCI-{period}'] = ta.cci(data['max_price'], data['min_price'], data['closing_price'],
                                       length=max(2, period))
        data[f'Momentum-{period}'] = ta.mom(data['closing_price'], length=period)

    # MACD
    macd_configs = [
        (1, 5, 12, 9),  # period, fast, slow, signal
        (7, 12, 26, 9),
        (30, 26, 50, 9)
    ]
    for period, fast, slow, signal in macd_configs:
        data[f'MACD-{period}'], data[f'Signal_{period}'], _ = ta.macd(data['closing_price'], fast=fast, slow=slow,
                                                                      signal=signal)

    return data


def generate_moving_average_signals(data):
    ma_types = ['SMA', 'EMA', 'WMA', 'HMA', 'VWMA']

    for ma_type in ma_types:
        for i in range(len(MOVING_AVERAGES_PERIODS) - 1):
            current_period = MOVING_AVERAGES_PERIODS[i]
            next_period = MOVING_AVERAGES_PERIODS[i + 1]
            data[f'Signal{ma_type}{current_period}'] = np.where(
                data[f'{ma_type}-{current_period}'] > data[f'{ma_type}-{next_period}'], 1, 0
            )


def generate_oscillator_signals(data, period):
    suffix = str(period)

    data[f'RSI-Signal-{suffix}'] = np.where(
        data[f'RSI-{period}'] > THRESHOLDS["RSI"]["overbought"], -1,
        np.where(data[f'RSI-{period}'] < THRESHOLDS["RSI"]["oversold"], 1, 0)
    )
    data[f'MACD-Signal-{suffix}'] = np.where(
        data[f'MACD-{period}'] > data[f'Signal_{period}'], 1, -1
    )
    data[f'CCI-Signal-{suffix}'] = np.where(
        data[f'CCI-{period}'] > THRESHOLDS["CCI"]["overbought"], -1,
        np.where(data[f'CCI-{period}'] < -THRESHOLDS["CCI"]["oversold"], 1, 0)
    )
    data[f'Momentum-Signal-{suffix}'] = np.where(
        data[f'Momentum-{period}'] > 0, 1, -1
    )

    return data


def aggregate_signals_for_decision(data, period):
    suffix = str(period)
    data[f'MA-Signal-{suffix}'] = sum(
        data[f'Signal{ma_type}{period}'] for ma_type in ['SMA', 'EMA', 'WMA', 'HMA', 'VWMA']
    )

    data[f'CombinedSignal-{suffix}'] = (
            WEIGHTS['MA'] * data[f'MA-Signal-{suffix}'] +
            WEIGHTS['RSI'] * data[f'RSI-Signal-{suffix}'] +
            WEIGHTS['MACD'] * data[f'MACD-Signal-{suffix}'] +
            WEIGHTS['CCI'] * data[f'CCI-Signal-{suffix}'] +
            WEIGHTS['Momentum'] * data[f'Momentum-Signal-{suffix}']
    )

    data[f'FinalDecision-{suffix}'] = np.where(
        data[f'CombinedSignal-{suffix}'] > THRESHOLDS['Decision'], 'Buy',
        np.where(data[f'CombinedSignal-{suffix}'] < -THRESHOLDS['Decision'], 'Sell', 'Hold')
    )

def perform_technical_analysis(company, period):
    try:
        data = load_stocks_as_dataframe(company)

        if len(data) < max(MOVING_AVERAGES_PERIODS):
            return "Error: Not enough data"

        compute_technical_indicators(data)
        generate_moving_average_signals(data)
        generate_oscillator_signals(data, period)
        aggregate_signals_for_decision(data, period)

        last_decisions = data[f'FinalDecision-{period}'].tail(period)
        buy_count = (last_decisions == 'Buy').sum()
        sell_count = (last_decisions == 'Sell').sum()

        if buy_count > sell_count:
            return 'Buy'
        elif sell_count > buy_count:
            return 'Sell'
        else:
            return 'Hold'

    except Exception as e:
        return f"Error: {str(e)}"
