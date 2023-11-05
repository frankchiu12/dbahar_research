import os
import pandas as pd
import re

# Path to the original CEO articles
new_path = r'E:\Research Project\CEO Articles Namewise (more_than_5)'

# Path to save preprocessed CEO articles
to_path = r'E:\Research Project\CEO Articles Preprocessed (more_than_5) v_2'

# Reading CSV
file = pd.read_csv(r"E:\Research Project\ceo_list.csv", encoding='utf-8')
file["CLEANED NAME v2"] = file["CLEANED NAME v2"].fillna('')
file["CLEANED NAME v3"] = file["CLEANED NAME v3"].fillna('')

# Create a list of CEO names
ceo_name = os.listdir(new_path)

# Lists to store different versions of CEO names
ceo_name_v_1 = []
ceo_name_v_2 = []
ceo_name_v_3 = []

# Creating v_1, v_2 and v_3 lists of CEO names
for i in range(len(ceo_name)):
    index = file[file["DirectorName"] == ceo_name[i]].index.tolist()[0]
    ceo_name_v_1.append(file.iloc[index][6])

    # Checking if cell is null in v_2
    is_null_2 = pd.isnull(file.iloc[index][7])
    if not is_null_2:
        ceo_name_v_2.append(file.iloc[index][7])
    else:
        ceo_name_v_2.append('')

    # Checking if cell is null in v_3
    is_null_3 = pd.isnull(file.iloc[index][8])
    if not is_null_3:
        ceo_name_v_3.append(file.iloc[index][8])
    else:
        ceo_name_v_3.append('')

# Processing each CEO article
for i in range(len(ceo_name)):
    ceo_path = os.path.join(new_path, ceo_name[i])
    txt_path = os.path.join(ceo_path, 'plaintext')
    txt_files = os.listdir(txt_path)

    # Lists to store name parts
    first_name = []
    middle_name = []
    last_name = []

    # Splitting the CEO names into parts
    temp_1 = ceo_name_v_1[i].lower().split()
    temp_2 = ceo_name_v_2[i].lower().split()
    temp_3 = ceo_name_v_3[i].lower().split()

    # Considering cases with and without middle names
    if len(temp_1) == 3:
        first_name.append(temp_1[0])
        middle_name.append(temp_1[1])
        last_name.append(temp_1[2])
    elif len(temp_1) == 2:
        first_name.append(temp_1[0])
        last_name.append(temp_1[1])

    temp_1 = temp_2[:]
    if len(temp_1) == 3:
        first_name.append(temp_1[0])
        middle_name.append(temp_1[1])
        last_name.append(temp_1[2])
    elif len(temp_1) == 2:
        first_name.append(temp_1[0])
        last_name.append(temp_1[1])

    temp_1 = temp_3[:]
    if len(temp_1) == 3:
        first_name.append(temp_1[0])
        middle_name.append(temp_1[1])
        last_name.append(temp_1[2])
    elif len(temp_1) == 2:
        first_name.append(temp_1[0])
        last_name.append(temp_1[1])

    # Create a search list from the name parts
    first_name = list(set(first_name))
    middle_name = list(set(middle_name))
    last_name = list(set(last_name))
    search_list = first_name + middle_name + last_name

    # Remove unnecessary terms like incomplete middle names
    search_list_final = []
    for element in search_list:
        if '.' in element:
            continue
        search_list_final.extend([element.lower(), f"{element.lower()}'s", f"{element.lower()}.", f"{element.lower()},"])

    # Opening text file of CEO
    for file in txt_files:
        file_path = os.path.join(txt_path, file)
        text_file = open(file_path, 'r+', encoding='utf-8')
        text = text_file.read()

        # Cleaning text (removing links and digits)
        only_text = ''.join(c for c in text if not c.isdigit())
        no_links = re.sub(r'http\S+', '', only_text)
        text = no_links

        # Creating new file's path
        new_temp_path = os.path.join(to_path, ceo_name[i])
        new_file_path = os.path.join(new_temp_path, 'plaintext')
        final_text_path = os.path.join(new_file_path, file)

        # Checking if word matches in paragraph or not
        # Dividing articles in paragraphs
        for paragraphs in text.split('\n'):
            found = 0
            num = len(paragraphs.strip().split())

            # Dividing paragraphs into words
            for word_index in range(num):
                word = paragraphs.strip().split()[word_index]

                # Checking if the word starts with a capital letter and is in search_list
                if word[0].isupper() and word.lower() in search_list_final:
                    word = ' ' + word + ' '
                    paragraphs = paragraphs.replace(word, f' ceo_name_{i} ')
                    found = 1

            # Writing the text to the new file destination having only the relevant text
            if found == 1:
                with open(final_text_path, 'a', encoding='utf-8') as f:
                    f.write(paragraphs + '\n')