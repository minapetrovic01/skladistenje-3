import os
import pandas as pd

train_test_dir = "../my_data/cic/"

all_train_data = pd.DataFrame()
all_test_data = pd.DataFrame()

for filename in os.listdir(train_test_dir):
    if filename.startswith("CICFLOWTRAIN_") and filename.endswith(".csv"):
        file_path = os.path.join(train_test_dir, filename)
        train_data = pd.read_csv(file_path)
        all_train_data = pd.concat([all_train_data, train_data], ignore_index=True)
    elif filename.startswith("CICFLOWTEST_") and filename.endswith(".csv"):
        file_path = os.path.join(train_test_dir, filename)
        test_data = pd.read_csv(file_path)
        all_test_data = pd.concat([all_test_data, test_data], ignore_index=True)

all_train_data.to_csv("ALL_CICFLOW_TRAIN.csv", index=False)
all_test_data.to_csv("ALL_CICFLOW_TEST.csv", index=False)

print("Combined train and test datasets saved as ALL_CICFLOW_TRAIN.csv and ALL_CICFLOW_TEST.csv respectively.")
