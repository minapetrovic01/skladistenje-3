import pandas as pd
from sklearn.model_selection import train_test_split
import os

folder_path = 'C:\\Users\\minap\\ELFAK\\skladistenje\\projekat3\\data'    

train_df = pd.read_csv(os.path.join(folder_path, 'ALL_CICFLOW_TRAIN_BIN.csv'))
test_df = pd.read_csv(os.path.join(folder_path, 'ALL_CICFLOW_TEST_BIN.csv'))

target_variable = 'classification'

sampled_train_df, _ = train_test_split(
    train_df,
    train_size=30000,
    stratify=train_df[target_variable],
    random_state=42
)

sampled_train_df.to_csv('C:\\Users\\minap\\ELFAK\\skladistenje\\projekat3\\data\\sampled_train_bin.csv', index=False)
test_df.to_csv('C:\\Users\\minap\\ELFAK\\skladistenje\\projekat3\\data\\sampled_test_bin.csv', index=False)

num_test_instances = test_df.shape[0]
print(f"Sampled train dataset saved as 'sampled_train.csv' with 30,000 instances.")
print(f"Test dataset saved as 'sampled_test.csv' with {num_test_instances} instances.")
