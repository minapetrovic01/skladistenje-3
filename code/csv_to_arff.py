import os
import pandas as pd

def convert_csv_to_arff(csv_file_path, arff_file_path, relation_name):
    df = pd.read_csv(csv_file_path)
    
    with open(arff_file_path, 'w') as f:
        f.write(f"@relation {relation_name}\n\n")
        
        for column in df.columns:
            f.write(f"@attribute {column} numeric\n")
        
        f.write("\n@data\n")
        
        for index, row in df.iterrows():
            f.write(','.join(map(str, row.values)) + '\n')

def convert_folder_of_csvs_to_arffs(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, file_name)
            arff_file_path = os.path.join(output_folder, file_name.replace('.csv', '.arff'))
            relation_name = os.path.splitext(file_name)[0]
            convert_csv_to_arff(csv_file_path, arff_file_path, relation_name)
            print(f"Converted {file_name} to {relation_name}.arff")

input_folder = '..\\data'  
output_folder = '..\\data\\arffs' 

convert_folder_of_csvs_to_arffs(input_folder, output_folder)
