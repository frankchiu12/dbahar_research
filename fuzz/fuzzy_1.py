import pandas as pd
from thefuzz import process

def read_csv_with_encoding(file_path, encoding='utf-8'):
    try:
        return pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='latin1')

unique_companies = read_csv_with_encoding('Unique_Companies.csv')
parents_dnb = read_csv_with_encoding('ParentsNameDunBradstreet.csv')

# Function to perform fuzzy matching and return the DUNS number and business name if a match is found
def get_best_match(company_name, threshold=90):
    # Check for exact match first
    exact_match = parents_dnb[parents_dnb['bizname'] == company_name]
    if not exact_match.empty:
        print('reaching1')
        return exact_match.iloc[0]['dunsnumber'], company_name

    # If no exact match, perform fuzzy matching
    best_match = process.extractOne(company_name, parents_dnb['bizname'].tolist(), score_cutoff=threshold)
    if best_match:
        match_info = parents_dnb[parents_dnb['bizname'] == best_match[0]]
        print('reaching2')
        return match_info.iloc[0]['dunsnumber'], best_match[0]
    else:
        print('reaching3')
        return "", ""

# Apply the fuzzy matching function to each row in the unique companies dataframe
match_results = unique_companies['Ultimate.Company'].apply(lambda x: pd.Series(get_best_match(x), index=['DUNS Number', 'Matched bizname']))

# Join the match results with the original unique companies DataFrame
unique_companies_with_matches = unique_companies.join(match_results)

# Adjust the output file path as needed
output_file_path = 'fuzz_output.csv'
unique_companies_with_matches.to_csv(output_file_path, index=False)