import os

import pandas as pd

from pandasgui import show

json_list = ['CA_category_id.json', 'DE_category_id.json', 'FR_category_id.json', 'GB_category_id.json',
             'IN_category_id.json', 'JP_category_id.json', 'KR_category_id.json', 'MX_category_id.json',
             'RU_category_id.json', 'US_category_id.json']
csv_list = ['CAvideos.csv', 'DEvideos.csv', 'FRvideos.csv', 'GBvideos.csv', 'INvideos.csv', 'JPvideos.csv',
            'KRvideos.csv', 'MXvideos.csv', 'RUvideos.csv', 'USvideos.csv']

country_abbrev = {'CA': 'Canada',
                  'DE': 'Germany',
                  'FR': 'France',
                  'GB': 'United Kingdom',
                  'IN': 'India',
                  'JP': 'Japan',
                  'KR': 'South Korea',
                  'MX': 'Mexico',
                  'RU': 'Russia',
                  'US': 'United States'}

df_list = []
for csv_name, json_name in zip(csv_list, json_list):
    csv_path = os.path.join('raw', csv_name)
    json_path = os.path.join('raw', json_name)

    print(csv_name)

    videos = pd.read_csv(csv_path, encoding="ISO-8859-1")
    categories_json = pd.read_json(json_path)

    categories_list = []
    for index, row in categories_json.iterrows():
        category_id = int(row['items']['id'])
        category_name = row['items']['snippet']['title']
        categories_list.append(
            {'category_id': category_id, 'category_name': category_name})

    categories_df = pd.DataFrame(categories_list)

    df = videos.merge(categories_df, on='category_id', how='left')

    df['country_code'] = csv_name[0:2]
    df['country'] = country_abbrev[csv_name[0:2]]
    df_list.append(df)

merged = pd.concat(df_list, axis=0)

merged['publish_time'] = pd.to_datetime(merged['publish_time'])
merged['trending_date'] = pd.to_datetime(
    merged['trending_date'], format="%y.%d.%m")

merged.to_csv('youtube_trending.csv', index=False)
