import pandas as pd
import numpy as np
import keras
import random
import tensorflow as tf
from keras.src.models import Sequential
from keras.src.layers import LSTM, Dense, Input
from keras import regularizers
from keras.src.callbacks import EarlyStopping
from keras.src.initializers import GlorotUniform
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import timedelta, datetime
from service.preprocess.stocks_preprocess import get_stocks_as_dataframe

random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)

def get_existing_predictions(company_name: str, csv_file: str = "future_stock_predictions.csv"):

    today = datetime.now().strftime("%Y-%m-%d")
    try:
        predictions_df = pd.read_csv(csv_file)
        if not predictions_df.empty:
            company_predictions = predictions_df[predictions_df["company"] == company_name]

            if company_predictions.empty:
                print(f"No predictions found for company {company_name}.")
                return None

            if "last_prediction" in company_predictions.columns:
                last_prediction_date = company_predictions["last_prediction"].iloc[0]
                if last_prediction_date == today:
                    prediction_dates = company_predictions.columns[2:]
                    return company_predictions[["company", "last_prediction", *prediction_dates]]

            print(f"Predictions for {company_name} are not up-to-date.")
            return None
    except FileNotFoundError:
        return None

def perform_lstm_analysis(company_name, steps, csv_file: str = "future_stock_predictions.csv"):

    def map_predictions_to_dates(predictions):
        base_date = datetime.now()
        return [
            {
                "company name": company_name,
                "date": (base_date + timedelta(days=int(day))).strftime("%Y-%m-%d"),
                "price": float(price.iloc[0]) if isinstance(price, pd.Series) else float(price)
            }
            for day, price in predictions.items() if day.isdigit()
        ]

    existing_predictions = get_existing_predictions(company_name, csv_file)
    if existing_predictions is not None:
        return map_predictions_to_dates(existing_predictions)

    data = get_stocks_as_dataframe(company_name)
    if data is None:
        return None

    data.index = pd.to_datetime(data.index)
    last_date = data.index[-1]
    today = datetime.now().strftime("%Y-%m-%d")

    full_date_range = pd.date_range(start=last_date, end=today)

    data_full = data.reindex(full_date_range)
    data_full.ffill(inplace=True)
    data = pd.concat([data, data_full[1:]])

    columns = data.columns.drop(['company', 'percentage_change', 'avg_price', 'total_turnover', 'volume'])
    lag = 5
    for i in range(1, lag + 1):
        for col in columns:
            data[f'{col}_prev_{i}'] = data[col].shift(i)
    data = data.dropna(axis=0)

    features = data.columns.drop(
        ['max_price', 'company', 'closing_price', 'avg_price', 'volume', 'min_price', 'percentage_change', 'total_turnover'])
    X, Y = data[features], data['closing_price']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, shuffle=False)
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    Y_train = scaler.fit_transform(Y_train.values.reshape(-1, 1))

    X_train = X_train.reshape(X_train.shape[0], lag, X_train.shape[1] // lag)
    X_test = X_test.reshape(X_test.shape[0], lag, X_test.shape[1] // lag)

    model = Sequential()
    model.add(Input(shape=(X_train.shape[1], X_train.shape[2])))

    model.add(LSTM(64, activation='relu',
                   kernel_initializer=GlorotUniform(seed=42),
                   kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4),
                   bias_regularizer=regularizers.L2(1e-4),
                   return_sequences=True))
    model.add(LSTM(32, activation='relu',
                   kernel_initializer=GlorotUniform(seed=42),
                   kernel_regularizer=regularizers.L2(1e-4),
                   bias_regularizer=regularizers.L2(1e-4)))
    model.add(Dense(1, activation='linear',
                    kernel_initializer=GlorotUniform(seed=42),
                    kernel_regularizer=regularizers.L2(1e-4)))

    model.compile(loss=keras.losses.MeanSquaredError(),
                  optimizer=keras.optimizers.Adam(learning_rate=0.001),
                  metrics=[keras.metrics.MeanSquaredError(), keras.metrics.MeanAbsoluteError()])

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
    model.fit(X_train, Y_train, validation_split=0.2, batch_size=32, epochs=50, callbacks=[early_stopping], shuffle=False)

    last_sequence = X_test[-1].reshape(1, lag, X_test.shape[2])

    def predict(Model, _last_sequence, steps, Scaler, min_price, max_price):
        prediction_list = []
        current_input = _last_sequence

        lower_bound = Scaler.transform([[min_price * 0.9]])[0][0]
        upper_bound = Scaler.transform([[max_price * 1.1]])[0][0]

        for step in range(steps):
            predicted_price = Model.predict(current_input)

            predicted_price = np.clip(predicted_price[0][0], lower_bound, upper_bound)
            prediction_list.append(predicted_price)

            predicted_price_reshaped = np.repeat(predicted_price.reshape(1, 1, 1), current_input.shape[2], axis=2)

            current_input = np.concatenate((predicted_price_reshaped, current_input[:, :-1, :]), axis=1)

        predictions_rescaled = Scaler.inverse_transform(np.array(prediction_list).reshape(-1, 1))
        return predictions_rescaled

    min_price = data['closing_price'].min()
    max_price = data['closing_price'].max()

    future_predictions = predict(model, last_sequence, steps, scaler, min_price, max_price)

    company_predictions = {
        "company": company_name,
        "last_prediction": today,
        **{str(i + 1): price for i, price in enumerate(future_predictions.flatten())}
    }

    try:
        predictions_df = pd.read_csv(csv_file)
    except FileNotFoundError:
        predictions_df = pd.DataFrame(columns=["company", "last_prediction", *(str(i + 1) for i in range(steps))])

    if "company" not in predictions_df.columns:
        predictions_df = pd.DataFrame(columns=["company", "last_prediction", *(str(i + 1) for i in range(steps))])


    predictions_df = predictions_df[predictions_df["company"] != company_name]
    predictions_df = pd.concat([predictions_df, pd.DataFrame([company_predictions])], ignore_index=True)

    predictions_df.to_csv(csv_file, index=False)

    return map_predictions_to_dates(company_predictions)