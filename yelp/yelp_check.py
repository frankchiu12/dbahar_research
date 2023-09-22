import json

# Replace 'your_large_json_file.json' with the path to your JSON file
json_file_path = '/Users/franksi-unchiu/Downloads/yelp_dataset/yelp_academic_dataset_review.json'

# Initialize a variable to store the latest date (assuming the first date is the latest initially)
latest_date = "0000-00-00"

# Open the JSON file and iterate through each JSON object
with open(json_file_path, 'r') as file:
    for line in file:
        data = json.loads(line)
        
        # Extract the date from the JSON object
        date_str = data.get("date", "")
        print(date_str)
        
        # Compare the extracted date with the current latest date
        if date_str > latest_date:
            latest_date = date_str

# Print the latest date found in the JSON file
print("Latest date:", latest_date)