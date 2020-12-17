import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

# kaggle data:
lap_times = pd.read_csv(r"F1_data\lap_times.csv")
drivers = pd.read_csv(r"F1_data\drivers.csv")
results = pd.read_csv(r"F1_data\results.csv")

# scraped data:
circuits = pd.read_csv(r"data_cleaned\circuits.csv")
races = pd.read_csv(r"data_cleaned\races.csv")
engines = pd.read_csv(r"data_cleaned\engines.csv")

# merged data:
teams = pd.read_csv(r"data_cleaned\teams.csv")
lap_speeds = pd.read_csv(r"data_cleaned\lap_speeds.csv")
main_drivers = pd.read_csv(r"data_cleaned\main_drivers .csv")
constructors = pd.read_csv(r"data_cleaned\constructors.csv")

df = lap_speeds[['raceId', 'year', 'driverId', 'lap', 'position', 'km_per_sec', 'km_per_min']]\
    .merge(races[['raceId', 'circuitId']], on ='raceId', how='left')
df = df.merge(teams[['raceId', 'driverId', 'constructorId', 'constructorRef_mapped']],
              on=['raceId', 'driverId'], how='left')
df = df.merge(circuits[['circuitId', 'circuitRef']], on='circuitId', how='left')

avg_lap_speed = pd.DataFrame({'avg_lap_speed': df.groupby(['year', 'constructorRef_mapped'])['km_per_min']\
              .mean()}).sort_values(['constructorRef_mapped', 'year']).reset_index()

avg_lap_speed = avg_lap_speed.sort_values(["constructorRef_mapped","year"])
avg_lap_speed = avg_lap_speed.merge(main_drivers, on = ['year', 'constructorRef_mapped'], how='left')
avg_lap_speed['drivers'] = avg_lap_speed.groupby(['year', 'constructorRef_mapped'])['surname']\
    .transform(lambda x : ', '.join(x))
avg_lap_speed = avg_lap_speed[['year', 'constructorRef_mapped', 'avg_lap_speed', 'drivers']].drop_duplicates()

avg_lap_speed.to_csv(r"graph_data\avg_lap_speed.csv", index=False)

# get min an max speeds throughout the time period:
max_speeds = avg_lap_speed.loc[avg_lap_speed.groupby(['year'])['avg_lap_speed'].idxmax()].reset_index(drop=True)
min_speeds = avg_lap_speed.loc[avg_lap_speed.groupby(['year'])['avg_lap_speed'].idxmin()].reset_index(drop=True)
max_speeds.to_csv(r"graph_data\max_speeds.csv", index=False)
min_speeds.to_csv(r"graph_data\min_speeds.csv", index=False)


# Data for barplot

winners = results.loc[results.positionOrder ==1, ['raceId', 'constructorId']]
winners = winners.merge(races.loc[races.year > 1995, ['raceId', 'year']], on='raceId', how='left')
winners = winners.merge(constructors[['constructorId', 'constructorRef_mapped']], on ='constructorId', how='left')
winners = winners.merge(engines[['year', 'engine', 'constructorId']], how='left',
                        left_on=['constructorId', 'year'],
                        right_on=['constructorId', 'year'])

expected = results[['raceId', 'constructorId', 'grid']].copy()
expected = expected.merge(races.loc[races.year > 1995, ['raceId', 'year']], on='raceId', how='inner')
expected = expected.merge(constructors[['constructorId', 'constructorRef_mapped']], on ='constructorId', how='left')
expected = expected.merge(engines[['year', 'engine', 'constructorId', 'constructorRef']], how='left',
                        left_on=['constructorId', 'year'],
                        right_on=['constructorId', 'year'])

engine_count  = pd.DataFrame({'engine_count' : expected.groupby(['engine', 'year'])['constructorId'].count()}).reset_index()
starter_count = pd.DataFrame({'starter_count' : expected.groupby(['year'])['constructorId'].count()}).reset_index()
race_count    = pd.DataFrame({'race_count' : expected.groupby(['year'])['raceId'].nunique()}).reset_index()
expected_vals = engine_count.merge(starter_count, how='left', on ='year')
expected_vals = expected_vals.merge(race_count, how='left', on ='year')
expected_vals['expected'] = expected_vals['engine_count']/expected_vals['starter_count']
expected_vals['expected wins'] = expected_vals['expected']*expected_vals['race_count']

engine_count_top3 = pd.DataFrame({'engine_count' : expected.groupby(['engine', 'year'])['constructorId'].nunique()}).reset_index()
engine_count_top3 = engine_count_top3[engine_count_top3.engine.isin(['mercedes', 'ferrari', 'renault'])]

engine_count_top3_piv = pd.pivot_table(engine_count_top3, values="engine_count", index="year", columns="engine")
engine_count_top3_piv.fillna(0, inplace=True)
engine_count_top3 = engine_count_top3_piv.stack().reset_index(name='engine_count')

top3 = winners.loc[winners.engine.isin(['mercedes', 'ferrari', 'renault'])]
top3_exp = expected_vals.loc[expected_vals.engine.isin(['mercedes', 'ferrari', 'renault'])]

top3_win_count = pd.DataFrame({'engine_win_count' : top3.groupby(['engine', 'year'])['raceId'].count()}).reset_index()

top3_piv = pd.pivot_table(top3_win_count, values="engine_win_count", index="year", columns="engine")
top3_exp_piv = pd.pivot_table(top3_exp, values="expected wins", index="year", columns="engine")

top3_piv.fillna(0, inplace=True)
top3_exp_piv.fillna(0, inplace=True)

top3 = top3_piv.stack().reset_index(name='engine_win_count')
top3_exp = top3_exp_piv.stack().reset_index(name='expected wins')

top3.to_csv(r"graph_data\top3.csv", index=False)
top3_exp.to_csv(r"graph_data\top3_exp.csv", index=False)
engine_count_top3.to_csv(r"graph_data\engine_count_top3.csv", index=False)



