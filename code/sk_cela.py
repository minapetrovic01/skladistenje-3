import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data_dir = "../CICIDS2017/MachineLearningCVE"
allData = pd.DataFrame()

# Load all datasets and concatenate them into a single DataFrame
for filename in os.listdir(data_dir):
    print(f"Processing file: {filename}")
    dataset = pd.read_csv(os.path.join(data_dir, filename))
    allData = pd.concat([allData, dataset], ignore_index=True)

# Replace mislabeled attack names and rename columns
allData[" Label"].replace(
    to_replace={
        "Web Attack � Brute Force": "Web Attack Brute Force",
        "Web Attack � XSS": "Web Attack XSS",
        "Web Attack � Sql Injection": "Web Attack Sql Injection",
    },
    inplace=True,
)
allData.rename(
    columns={
        " Flow Packets/s": "Flow_Packets",
        "Flow Bytes/s": "Flow_Bytes",
        " Label": "classification",
    },
    inplace=True,
)

# Handle infinite values and missing data
allData.replace([np.inf, -np.inf], np.nan, inplace=True)
allData.dropna(inplace=True)

print(allData["classification"].count())
print(allData["classification"].value_counts())

os.abort()

# Define lists for column types
cls = "classification"
listNominal = []
listBinary = []
listNumerical = list(set(allData.columns) - set(listNominal) - set(listBinary))
listNumerical.remove(cls)

# StandardScaler for numerical columns
scaler = StandardScaler()

# Separate BENIGN and attack data
benign_data = allData[allData["classification"] == "BENIGN"]
attack_data = allData[allData["classification"] != "BENIGN"]

# Ensure balanced data
min_len = min(len(benign_data), len(attack_data))

benign_data = benign_data.sample(min_len)
attack_data = attack_data.sample(min_len)

combined_data = pd.concat([benign_data, attack_data])

# Split into train and test datasets
train_df, test_df = train_test_split(
    combined_data, test_size=0.2, stratify=combined_data["classification"]
)

# Scale numerical columns
train_df[listNumerical] = scaler.fit_transform(train_df[listNumerical])
test_df[listNumerical] = scaler.transform(test_df[listNumerical])

# Save the combined datasets into single CSV files
train_df.to_csv("ALL_CICFLOW_TRAIN.csv", index=False)
test_df.to_csv("ALL_CICFLOW_TEST.csv", index=False)

print("Combined train and test datasets saved as ALL_CICFLOW_TRAIN.csv and ALL_CICFLOW_TEST.csv respectively.")
