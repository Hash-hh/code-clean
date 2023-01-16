import os
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


# # Load the time series data
# data = sm.datasets.sunspots.load_pandas().data
#
# # Split the data into training and testing sets
# train_data = data[:int(0.8*len(data))]['SUNACTIVITY']
# test_data = data[int(0.8*len(data)):]['SUNACTIVITY']
#
# print(train_data[0])
# print(type(train_data))
# print(type(train_data[0]))
#
# # Fit an AR model to the training data
# model = sm.tsa.AutoReg(train_data, lags=0).fit()
#
# # Make predictions on the test data
# predictions = model.predict(start=test_data.index[0], end=test_data.index[-1])
#
# print(test_data.index[0])
# print(test_data.index[-1])
#
#
# # Plot the actual values and predictions
# plt.plot(test_data, label='Actual values')
# plt.plot(predictions, label='Predictions')
# plt.legend()
# plt.show()

def train_model(resampled_path, generated_path, predicted_path, figures_path, train_csv):
    train_csv_file = f'{resampled_path}/{train_csv}'  # training on the resampled file
    all_predict_csvs = os.listdir(f'{predicted_path}/{train_csv.split("_")[0]}')  # predict on these csvs
    df = pd.read_csv(train_csv_file, header=None)
    raw_seq = pd.Series(df.iloc[:, 1])
    num_of_models = len(all_predict_csvs)

    for i in range(num_of_models):

        # Fit an AR model to the training data
        model = sm.tsa.ARIMA(raw_seq, order=(3,3,3)).fit()

        print("predicting on " + all_predict_csvs[i])

        # Make predictions on the test data
        pred_df = pd.read_csv(f'{predicted_path}/{train_csv.split("_")[0]}/{all_predict_csvs[i]}', header=None)
        # pred_raw = pred_df[1].to_numpy()
        pred_raw = pd.Series(pred_df.iloc[:, 1])

        print("start: ", pred_raw.index[0])

        predictions = model.predict(start=pred_raw.index[0], end=pred_raw.index[-1])

        outpath = f'{generated_path}/{train_csv.split("_")[0]}'
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        pd.DataFrame(predictions.tolist(), index=pred_df[0]).to_csv(f'{outpath}/{all_predict_csvs[i]}',
                                                        header=False)  # dump files in the generated folder

        # Plot the actual values and predictions
        plt.plot(pred_raw, label='Actual values')
        plt.plot(predictions, label='Predictions')
        plt.legend()
        plt.savefig(f'{figures_path}/{train_csv.split("_")[0]}.png')


def ARIMA_run(log_csv_file_name):
    print("Auto Regression training...")

    resampled_path = 'data/csvs/' + log_csv_file_name + '/resampled/'
    generated_path = 'data/csvs/' + log_csv_file_name + '/generated/' + 'ARIMA/'
    predicted_path = 'data/csvs/' + log_csv_file_name + '/predicted_data/'
    figures_path = 'data/csvs/' + log_csv_file_name + '/figures/' + 'ARIMA/'

    if not os.path.exists(generated_path):
        os.makedirs(generated_path)
    if not os.path.exists(figures_path):
        os.makedirs(figures_path)

    for train_csv in os.listdir(resampled_path):
        print("training on ", train_csv)
        train_model(resampled_path, generated_path, predicted_path, figures_path, train_csv)
    print('\n')
