import os
import pandas as pd

def sanitize_attribute_name(name):
    return ''.join(['_' if c in ' !@#$%^&*()[]{};:,./<>?\|`~-=+' else c for c in name])

def determine_attribute_type(column_data, column_name, class_attribute):
    if column_name == class_attribute:
        categories = column_data.unique()
        categories_str = ','.join([f"'{cat}'" for cat in categories])
        return f'{{{categories_str}}}'
    elif pd.api.types.is_numeric_dtype(column_data):
        return 'numeric'
    elif pd.api.types.is_string_dtype(column_data):
        return 'string'
    elif pd.api.types.is_categorical_dtype(column_data):
        categories = column_data.cat.categories
        categories_str = ','.join([f"'{cat}'" for cat in categories])
        return f'{{{categories_str}}}'
    else:
        raise ValueError(f"Unsupported attribute type for column {column_data.name}")

def convert_csv_to_arff(csv_file_path, arff_file_path, relation_name, class_attribute):
    df = pd.read_csv(csv_file_path)
    
    if class_attribute in df.columns:
        df[class_attribute] = df[class_attribute].astype(str).astype('category')
    else:
        raise ValueError(f"Classification attribute '{class_attribute}' not found in CSV file.")
    
    for column in df.columns:
        if column != class_attribute and not (pd.api.types.is_numeric_dtype(df[column]) or pd.api.types.is_string_dtype(df[column])):
            df[column] = df[column].astype('category')
    
    with open(arff_file_path, 'w') as f:
        f.write(f"@relation {relation_name}\n\n")
        
        for column in df.columns:
            sanitized_column = sanitize_attribute_name(column)
            attribute_type = determine_attribute_type(df[column], column, class_attribute)
            f.write(f"@attribute {sanitized_column} {attribute_type}\n")
        
        f.write("\n@data\n")
        
        for index, row in df.iterrows():
            row_str = []
            for value in row:
                if pd.isnull(value):
                    row_str.append('?')
                elif isinstance(value, str):
                    row_str.append(f"'{value}'")
                else:
                    row_str.append(str(value))
            f.write(','.join(row_str) + '\n')

def convert_folder_of_csvs_to_arffs(folder_path, output_folder, class_attribute):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, file_name)
            arff_file_path = os.path.join(output_folder, file_name.replace('.csv', '.arff'))
            relation_name = os.path.splitext(file_name)[0]
            convert_csv_to_arff(csv_file_path, arff_file_path, relation_name, class_attribute)
            print(f"Converted {file_name} to {relation_name}.arff")

# input_folder = '..\\data\\arffs3'  
# output_folder = '..\\data\\arffs3' 
input_folder = 'C:\\Users\\minap\\ELFAK\\skladistenje\\projekat3\\data\\arffs3'
output_folder = 'C:\\Users\\minap\\ELFAK\\skladistenje\\projekat3\\data\\arffs3'
class_attribute = 'classification'  

convert_folder_of_csvs_to_arffs(input_folder, output_folder, class_attribute)
