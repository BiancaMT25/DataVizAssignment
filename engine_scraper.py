import pandas as pd
from data_maps import reversed_constructor_map_engines

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

constructors = pd.read_csv(r"F1_data\constructors.csv")

link_start = 'https://en.wikipedia.org/wiki/'
link_end = '_Formula_One_World_Championship'

# Loop that scrapes engine data from wikipedia since 1996:
engine_df = pd.DataFrame()
for year in range(1996, 2021):
    link = link_start + str(year) + link_end
    df = pd.read_html(link)[1]
    if 'Entrant' not in df.columns:
        df = pd.read_html(link)[2]
        if 'Entrant' not in df.columns:
            df = pd.read_html(link)[3]
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel()
    tab = df.iloc[:, :4].copy()
    tab['year'] = year
    tab['url'] = link
    engine_df = pd.concat([engine_df, tab])


# data cleaning
engine_df2 = engine_df.loc[:, ['Constructor', 'year']]
engine_df2 = engine_df2.drop_duplicates()
engine_df2.dropna(axis=0, inplace=True)
engine_df2['Constructor'] = engine_df2['Constructor'].str.lower()
engine_df2 = engine_df2[~engine_df2.Constructor.str.contains("source")].copy()

engine_df2['Constructor'] = engine_df2['Constructor'].apply(lambda x: x.replace("\xa0", ""))
engine_df2['Constructor'] = engine_df2['Constructor'].apply(lambda x: x.replace("[18]", ""))
engine_df2['constructor_name'] = engine_df2['Constructor'].apply(lambda x: x.split("-")[0])
engine_df2['engine'] = engine_df2['Constructor'].apply(lambda x: x.split("-")[1] if "-" in x else x)


constructors['name'] = constructors['name'].str.lower()

# merge scraped constructor name with 'name' from constructors df
engine_df3 = engine_df2.merge(constructors[['constructorId', 'name', 'constructorRef']],
                              right_on='name', left_on='constructor_name', how='left')

# map the constructors that couldn't be matched to their names in the constructors df
engine_df3.loc[engine_df3.name.isnull(), 'constructor_name'] = \
    engine_df3.loc[engine_df3.name.isnull(), 'constructor_name'].map(reversed_constructor_map_engines)

# repeat merge with the mapped names to get the missing constructor names
engine_df3 = engine_df3.merge(constructors[['constructorId', 'name', 'constructorRef']],
                              right_on='name', left_on='constructor_name', how='left')

# keep the updated constructor ids and refs
engine_df4 = engine_df3[['Constructor', 'year', 'engine', 'constructorId_y', 'name_y', 'constructorRef_y']]

# save the useful columns
engine_df4.columns = ['Constructor', 'year', 'engine', 'constructorId', 'name', 'constructorRef']

# additional cleaning where engine data was missing or a different name
engine_df4.loc[engine_df4['engine'] == 'toro rosso', 'engine'] = 'renault'
engine_df4.loc[engine_df4['engine'] == 'bwt mercedes', 'engine'] = 'mercedes'
engine_df4.loc[engine_df4['engine'] == 'bmw sauber', 'engine'] = 'bmw'

engine_df4.to_csv(r"data_cleaned\engines.csv", index=False)