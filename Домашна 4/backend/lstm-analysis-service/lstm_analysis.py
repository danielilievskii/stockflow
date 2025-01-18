import pandas as pd
import numpy as np
import keras
import random
import tensorflow as tf
from datetime import timedelta, datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Input, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from stocks.stock_data_loader import load_stocks_as_dataframe

random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)

def get_existing_predictions(company_name: str, csv_file: str = "future_stock_predictions.csv"):
    try:
        predictions_df = pd.read_csv(csv_file)
    except FileNotFoundError:
        return None

    today = datetime.now().strftime("%Y-%m-%d")
    company_predictions = predictions_df[predictions_df["company"] == company_name]

    if not company_predictions.empty and company_predictions["last_prediction"].iloc[0] == today:
        return company_predictions

    return None


def format_predictions(predictions, company_name):
    base_date = datetime.now()
    return [
        {
            "company name": company_name,
            "date": (base_date + timedelta(days=int(day))).strftime("%Y-%m-%d"),
            "price": float(price.iloc[0]) if isinstance(price, pd.Series) else float(price)
        }
        for day, price in predictions.items() if day.isdigit()
    ]


def create_lag_features(data, lag, excluded_columns):
    data.index = pd.to_datetime(data.index)
    today = datetime.now().strftime("%Y-%m-%d")

    full_date_range = pd.date_range(start=data.index[-1], end=today)
    data_full = data.reindex(full_date_range).ffill()
    data = pd.concat([data, data_full[1:]])

    feature_columns = data.columns.difference(excluded_columns)

    for i in range(1, lag + 1):
        for col in feature_columns:
            data[f'{col}_prev_{i}'] = data[col].shift(i)

    return data.dropna()


def build_lstm_model(input_shape):
    model = Sequential([
        Input(shape=input_shape),
        LSTM(64, activation='relu',
             return_sequences=True),
        Dropout(0.2),
        LSTM(32, activation='relu'),
        Dropout(0.2),
        Dense(1, activation='linear')
    ])
    model.compile(loss=keras.losses.MeanSquaredError(),
                  optimizer=keras.optimizers.Adam(learning_rate=0.001),
                  metrics=[keras.metrics.MeanSquaredError(), keras.metrics.MeanAbsoluteError()])
    return model


def generate_future_predictions(model, last_sequence, steps, scaler, min_price, max_price):
    predictions = []
    current_input = last_sequence

    lower_bound = scaler.transform([[min_price * 0.95]])[0][0]
    upper_bound = scaler.transform([[max_price * 1.05]])[0][0]

    for step in range(steps):
        predicted_price = model.predict(current_input, verbose=0)[0][0]
        predicted_price = np.clip(predicted_price, lower_bound, upper_bound)
        predictions.append(predicted_price)

        predicted_price_reshaped = np.repeat(predicted_price.reshape(1, 1, 1), current_input.shape[2], axis=2)
        current_input = np.concatenate((predicted_price_reshaped, current_input[:, :-1, :]), axis=1)

    predictions_rescaled = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions_rescaled


def save_predictions_to_csv(predictions, file_path):
    try:
        predictions_df = pd.read_csv(file_path)
    except FileNotFoundError:
        predictions_df = pd.DataFrame(
            columns=["company", "last_prediction", *(str(i + 1) for i in range(len(predictions)))])

    predictions_df = predictions_df[predictions_df["company"] != predictions["company"]]
    predictions_df = pd.concat([predictions_df, pd.DataFrame([predictions])], ignore_index=True)
    predictions_df.to_csv(file_path, index=False)


def perform_lstm_analysis(company_name, steps, file_path: str = "future_stock_predictions.csv"):
    existing_predictions = get_existing_predictions(company_name, file_path)
    if existing_predictions is not None:
        return format_predictions(existing_predictions, company_name)

    stock_data = load_stocks_as_dataframe(company_name)
    if stock_data is None:
        return None

    lag = 5
    excluded_columns = ['company', 'percentage_change', 'avg_price', 'total_turnover', 'volume']
    processed_data = create_lag_features(stock_data, lag, excluded_columns)

    feature_columns = processed_data.columns.difference(['max_price', 'company', 'closing_price', 'avg_price',
                                                         'volume', 'min_price', 'percentage_change', 'total_turnover'])
    X = processed_data[feature_columns]
    Y = processed_data['closing_price']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, shuffle=False)
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train).reshape(X_train.shape[0], lag, X_train.shape[1] // lag)
    X_test = scaler.transform(X_test).reshape(X_test.shape[0], lag, X_test.shape[1] // lag)
    Y_train = scaler.fit_transform(Y_train.values.reshape(-1, 1))

    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=2,
        restore_best_weights=True
    )
    model.fit(X_train, Y_train, validation_split=0.2, batch_size=32, epochs=8, callbacks=[early_stopping],
              shuffle=False)

    last_sequence = X_test[-1].reshape(1, lag, X_test.shape[2])
    min_price = stock_data['closing_price'].min()
    max_price = stock_data['closing_price'].max()

    future_predictions = generate_future_predictions(model, last_sequence, steps, scaler, min_price, max_price)

    predictions_data = {
        "company": company_name,
        "last_prediction": datetime.now().strftime("%Y-%m-%d"),
        **{str(i + 1): float(price) for i, price in enumerate(future_predictions.flatten())}
    }

    save_predictions_to_csv(predictions_data, file_path)

    return format_predictions(predictions_data, company_name)
