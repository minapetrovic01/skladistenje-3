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

# Filter the dataset to include only the selected attacks and BENIGN class
selected_classes = ["DoS Slowhttptest", "SSH-Patator", "DoS Hulk", "PortScan", "FTP-Patator"]
filtered_data = allData[allData["classification"].isin(selected_classes)]

# Handle infinite values and missing data
filtered_data.replace([np.inf, -np.inf], np.nan, inplace=True)
filtered_data.dropna(inplace=True)

print(filtered_data["classification"].count())
print(filtered_data["classification"].value_counts())

# Define lists for column types
cls = "classification"
listNominal = []
listBinary = []
listNumerical = list(set(filtered_data.columns) - set(listNominal) - set(listBinary))
listNumerical.remove(cls)

# StandardScaler for numerical columns
scaler = StandardScaler()

# Create a balanced dataset
balanced_data = pd.DataFrame()

# Minimum number of samples in the smallest class
min_samples = min([len(filtered_data[filtered_data["classification"] == cls]) for cls in selected_classes])

# Sample min_samples from each selected class
for cls in selected_classes:
    class_data = filtered_data[filtered_data["classification"] == cls].sample(min_samples, random_state=42)
    balanced_data = pd.concat([balanced_data, class_data])

# Split into train and test datasets
train_df, test_df = train_test_split(
    balanced_data, test_size=0.2, stratify=balanced_data["classification"], random_state=42
)

# Scale numerical columns
train_df[listNumerical] = scaler.fit_transform(train_df[listNumerical])
test_df[listNumerical] = scaler.transform(test_df[listNumerical])

# Save the combined datasets into single CSV files
train_df.to_csv("ALL_CICFLOW_TRAIN_MULTI_NO_BEN.csv", index=False)
test_df.to_csv("ALL_CICFLOW_TEST_MULTI_NO_BEN.csv", index=False)

print("Combined train and test datasets saved as ALL_CICFLOW_TRAIN.csv and ALL_CICFLOW_TEST.csv respectively.")
