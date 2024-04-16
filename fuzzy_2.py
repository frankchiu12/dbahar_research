from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np

# Assuming you have a DataFrame df with columns Ultimate.Company, Company_N, DUNS Number, and Matched bizname
df = pd.read_csv('fuzz_output.csv')

# Define a function to calculate the similarity between two strings, considering null values
def calculate_similarity(row):
    # Check if any of the fields is null
    if pd.isnull(row['Ultimate.Company']) or pd.isnull(row['Matched bizname']):
        return np.nan  # Return NaN if any field is null
    else:
        return fuzz.ratio(row['Ultimate.Company'].lower(), row['Matched bizname'].lower())

# Apply the function to compare strings in each row and store the result in a new column
df['fuzz_score'] = df.apply(calculate_similarity, axis=1)

# Save the DataFrame back to a CSV file if needed
df.to_csv('fuzz_output.csv', index=False)