import pandas as pd
import pycountry

file1 = pd.read_csv('name2nat/name.csv')
file2 = pd.read_csv('name2nat/nat.csv')

combined_data = pd.concat([file1, file2], axis=1)
combined_data.columns = ['Name', 'Nationality']

to_merge_df = pd.read_csv('name2nat/inventors_names_nat_res_100ksample.csv')
to_merge_df.rename(columns={'STATE_OF_RESIDENCE_CODE': 'Nationality_Code'}, inplace=True)

nationality_mapping = {
    'American': 'United States',
    'English': 'United Kingdom',
    'British': 'United Kingdom',
    'Japanese': 'Japan',
    'German': 'Germany',
    'French': 'France',
    'Chinese': 'China',
    'Russian': 'Russia',
    'Indian': 'India',
    'Italian': 'Italy',
    'Spanish': 'Spain',
    'Canadian': 'Canada',
    'Australian': 'Australia',
    'Mexican': 'Mexico',
    'Brazilian': 'Brazil',
    'Argentinian': 'Argentina',
    'Swiss': 'Switzerland',
    'Swedish': 'Sweden',
    'Dutch': 'Netherlands',
    'Norwegian': 'Norway',
    'Danish': 'Denmark',
    'Austrian': 'Austria',
    'Belgian': 'Belgium',
    'Portuguese': 'Portugal',
    'Greek': 'Greece',
    'Turkish': 'Turkey',
    'Israeli': 'Israel',
    'Irish': 'Ireland',
    'Scottish': 'Scotland',
    'Welsh': 'Wales',
    'Finnish': 'Finland',
    'Polish': 'Poland',
    'Czech': 'Czech Republic',
    'Hungarian': 'Hungary',
    'South African': 'South Africa',
    'Korean': 'South Korea',
    'North Korean': 'North Korea',
    'Thai': 'Thailand',
    'Indonesian': 'Indonesia',
    'Vietnamese': 'Vietnam',
    'Philippine': 'Philippines',
    'Malaysian': 'Malaysia',
    'Singaporean': 'Singapore',
    'Saudi': 'Saudi Arabia',
    'Emirati': 'United Arab Emirates',
    'Qatari': 'Qatar',
    'Kuwaiti': 'Kuwait',
    'Omani': 'Oman',
    'Bahraini': 'Bahrain',
    'Lebanese': 'Lebanon',
    'Jordanian': 'Jordan',
    'Syrian': 'Syria',
    'Iraqi': 'Iraq',
    'Iranian': 'Iran',
    'Afghan': 'Afghanistan',
    'Pakistani': 'Pakistan',
    'Bangladeshi': 'Bangladesh',
    'Sri Lankan': 'Sri Lanka',
    'Nepali': 'Nepal',
    'Bhutanese': 'Bhutan',
    'Myanmar': 'Myanmar',
    'Laotian': 'Laos',
    'Cambodian': 'Cambodia',
    'Mongolian': 'Mongolia',
    'Uzbek': 'Uzbekistan',
    'Tajik': 'Tajikistan',
    'Turkmen': 'Turkmenistan',
    'Kazakh': 'Kazakhstan',
    'Kyrgyz': 'Kyrgyzstan',
    'Estonian': 'Estonia',
    'Latvian': 'Latvia',
    'Lithuanian': 'Lithuania',
    'Croatian': 'Croatia',
    'Bosnian': 'Bosnia and Herzegovina',
    'Serbian': 'Serbia',
    'Montenegrin': 'Montenegro',
    'Albanian': 'Albania',
    'Macedonian': 'North Macedonia',
    'Kosovan': 'Kosovo',
    'Slovenian': 'Slovenia',
    'Georgian': 'Georgia',
    'Armenian': 'Armenia',
    'Azerbaijani': 'Azerbaijan',
    'Moldovan': 'Moldova',
    'Belarusian': 'Belarus',
    'Ukrainian': 'Ukraine',
    'Ecuadorian': 'Ecuador',
    'Peruvian': 'Peru',
    'Chilean': 'Chile',
    'Colombian': 'Colombia',
    'Venezuelan': 'Venezuela',
    'Uruguayan': 'Uruguay',
    'Paraguayan': 'Paraguay',
    'Bolivian': 'Bolivia',
    'Costa Rican': 'Costa Rica',
    'Panamanian': 'Panama',
    'Nicaraguan': 'Nicaragua',
    'Honduran': 'Honduras',
    'Salvadoran': 'El Salvador',
    'Guatemalan': 'Guatemala',
    'Cuban': 'Cuba',
    'Haitian': 'Haiti',
    'Dominican': 'Dominican Republic',
    'Puerto Rican': 'Puerto Rico',
    'Jamaican': 'Jamaica',
    'Barbadian': 'Barbados',
    'Trinidadian': 'Trinidad and Tobago',
    'Guyanese': 'Guyana',
    'Surinamese': 'Suriname',
    'Bahamian': 'The Bahamas',
    'Belizean': 'Belize',
    'St. Lucian': 'Saint Lucia',
    'Antiguan': 'Antigua and Barbuda',
    'Kittitian': 'Saint Kitts and Nevis',
    'Vincentian': 'Saint Vincent and the Grenadines',
    'Grenadian': 'Grenada',
    'Dominican': 'Dominica',
    'Lucian': 'Saint Lucia',
    'Guinean': 'Guinea',
    'Sierra Leonean': 'Sierra Leone',
    'Liberian': 'Liberia',
    'Ivorian': "Côte d'Ivoire",
    'Ghanaian': 'Ghana',
    'Burkinabe': 'Burkina Faso',
    'Togolese': 'Togo',
    'Beninese': 'Benin',
    'Nigerien': 'Niger',
    'Senegalese': 'Senegal',
    'Malian': 'Mali',
    'Mauritanian': 'Mauritania',
    'Mauritian': 'Mauritius',
    'Seychellois': 'Seychelles',
    'Chadian': 'Chad',
    'Central African': 'Central African Republic',
    'Cameroonian': 'Cameroon',
    'Gabonese': 'Gabon',
    'Congolese': 'Republic of the Congo',
    'Equatorial Guinean': 'Equatorial Guinea',
    'São Toméan': 'São Tomé and Príncipe',
    'Angolan': 'Angola',
    'Namibian': 'Namibia',
    'Botswanan': 'Botswana',
    'Swazi': 'Eswatini (Swaziland)',
    'South Sudanese': 'South Sudan',
    'Sudanese': 'Sudan',
    'Eritrean': 'Eritrea',
    'Djiboutian': 'Djibouti',
    'Somali': 'Somalia',
    'Dane': 'Denmark',
    'Egyptian': 'Egypt',
    'Burmese': 'Myanmar',
    'Romanian': 'Romania',
    'Argentine': 'Argentina',
    'Bulgarian': 'Bulgaria',
    'Syriac': 'Syria'
}

iso_countries = {
    country.alpha_2: country.name for country in pycountry.countries
}
df_countries = pd.DataFrame(list(iso_countries.items()), columns=['Nationality_Code', 'Nationality'])

df_merged = pd.merge(to_merge_df, df_countries, on='Nationality_Code', how='left')
df_merged.drop(columns=['Nationality_Code', 'Unnamed: 0'], inplace=True)

def rearrange_name(name):
    parts = name.split(', ')
    if len(parts) > 1 and parts[0].isupper():
        return ' '.join(parts[1:]) + ' ' + parts[0]
    else:
        return name

df_merged['NAME'] = df_merged['NAME'].apply(rearrange_name)
df_merged.rename(columns={'NAME': 'Name'}, inplace=True)

combined_data['Nationality'] = combined_data['Nationality'].map(nationality_mapping)

df_merged.drop(columns=['NATIONALITY_STATE_CODE'], inplace=True)
combined_df = pd.concat([df_merged, combined_data], ignore_index=True)

combined_df.dropna(inplace=True)
combined_df.to_csv('name2nat/name_to_nat.csv', index=False)