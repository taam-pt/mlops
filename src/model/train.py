# Import libraries

import argparse
import glob
import os
# xfrom re import X
# from mlflow.tracking import MlflowClient

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import mlflow


# define functions
def main(args):
    # TO DO: enable autologging
    mlflow.autolog()
    run = mlflow.start_run()
    run_id = run.info.run_id

    # read data
    df = get_csvs_df(args.training_data)

    # split data
    X_train, X_test, y_train, y_test = split_data(df)

    # train model
    train_model(args.reg_rate, X_train, X_test, y_train, y_test)

    # finished_mlflow_run = MlflowClient().get_run(run_id)

    # metrics = finished_mlflow_run.data.metrics
    # tags = finished_mlflow_run.data.tags
    # params = finished_mlflow_run.data.params

    # print(run_id,metrics,tags,params)

    # the model folder produced from a run is registered. This includes the
    # MLmodel file, model.pkl and the conda.yaml.
    model_path = "model"
    model_uri = 'runs:/{}/{}'.format(run_id, model_path)
    mlflow.register_model(model_uri, "Model_diabetes")


def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided : {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


# TO DO: add function to split data
def split_data(df):
    X = df.drop('Diabetic', axis=1)
    X = X.drop('PatientID', axis=1)
    Y = df.Diabetic
    return train_test_split(X, Y, test_size=0.33, random_state=42)


def train_model(reg_rate, X_train, X_test, y_train, y_test):
    # train model
    LogisticRegression(C=1/reg_rate, solver="liblinear").fit(X_train, y_train)


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)
    parser.add_argument("--reg_rate", dest='reg_rate',
                        type=float, default=0.01)

    # parse args
    args = parser.parse_args()

    # return args
    return args


# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")
