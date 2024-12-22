import pandas as pd
import numpy as np
import keras
from keras.src.models import Sequential
from keras.src.layers import LSTM, Dense
from keras import regularizers
from keras.src.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import timedelta, datetime
from app.service.preparation.preparation import get_stocks_as_dataframe


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

def process_and_predict_for_company(company_name, csv_file: str = "future_stock_predictions.csv"):
    print(f"Processing company: {company_name}")

    existing_predictions = get_existing_predictions(company_name, csv_file)
    if existing_predictions is not None:
        print(f"Predictions for {company_name} are already up-to-date for today.")
        return existing_predictions

    data = get_stocks_as_dataframe(company_name)
    if data is None:
        print(f"Not enough data for company {company_name}.")
        return None

    columns = data.columns.drop(['company', 'percentage_change', 'avg_price', 'total_turnover', 'volume'])
    lag = 5
    for i in range(1, lag + 1):
        for col in columns:
            data[f'{col}_prev_{i}'] = data[col].shift(i)
    data = data.dropna(axis=0)

    features = data.columns.drop(
        ['max_price', 'company', 'closing_price', 'avg_price', 'volume', 'min_price', 'percentage_change', 'total_turnover'])
    X, Y = data[features], data['closing_price']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, shuffle=False, random_state=42)
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    Y_train = scaler.fit_transform(Y_train.values.reshape(-1, 1))

    X_train = X_train.reshape(X_train.shape[0], lag, X_train.shape[1] // lag)
    X_test = X_test.reshape(X_test.shape[0], lag, X_test.shape[1] // lag)

    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2]),
                   kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4), bias_regularizer=regularizers.L2(1e-4),
                   return_sequences=True))
    model.add(LSTM(50, activation='relu', kernel_regularizer=regularizers.L2(1e-4), bias_regularizer=regularizers.L2(1e-4)))
    model.add(Dense(1, activation='linear', kernel_regularizer=regularizers.L2(1e-4)))
    model.compile(loss=keras.losses.MeanSquaredError(),
                  optimizer=keras.optimizers.Adam(learning_rate=0.001),
                  metrics=[keras.metrics.MeanSquaredError(), keras.metrics.MeanAbsoluteError()])

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )
    model.fit(X_train, Y_train, validation_split=0.2, batch_size=32, epochs=50, callbacks=[early_stopping], shuffle=False)

    last_sequence = X_test[-1].reshape(1, lag, X_test.shape[2])

    def predict(Model, _last_sequence, steps, Scaler):
        prediction_list = []
        current_input = _last_sequence

        for _ in range(steps):
            predicted_price = Model.predict(current_input)
            prediction_list.append(predicted_price[0][0])

            predicted_price_reshaped = np.repeat(predicted_price.reshape(1, 1, 1), current_input.shape[2], axis=2)

            current_input = np.concatenate((predicted_price_reshaped, current_input[:, :-1, :]), axis=1)

        predictions_rescaled = Scaler.inverse_transform(np.array(prediction_list).reshape(-1, 1))
        return predictions_rescaled

    future_predictions = predict(model, last_sequence, 3, scaler)

    today = datetime.now()
    predicted_dates = [(today + timedelta(days=i + 1)).strftime("%Y-%m-%d") for i in range(3)]

    company_predictions = {
        "company": company_name,
        "last_prediction": datetime.now().strftime("%Y-%m-%d"),
        **{date: price for date, price in zip(predicted_dates, future_predictions.flatten())}
    }

    predictions_df = pd.DataFrame([company_predictions])
    predictions_df.to_csv(csv_file, mode='a', index=False, header=not pd.io.common.file_exists(csv_file))

    print(f"Predictions for {company_name}: {company_predictions}")
    return company_predictions