# Data on the actual team and constructor combination is not provided
# Teams are obtained by getting driverId and constructorID from race results
# The raceId is then used to get year to determine the constructor driver combination

import pandas as pd
from data_maps import reversed_constructor_map

constructors = pd.read_csv(r"F1_data\constructors.csv")
results = pd.read_csv(r"F1_data\results.csv")
drivers = pd.read_csv(r"F1_data\drivers.csv")
races = pd.read_csv(r"F1_data\races.csv")

teams = results[['raceId', 'driverId', 'constructorId', 'positionOrder']] \
    .merge(right=constructors[['constructorId', 'constructorRef']], on='constructorId', how='outer')
teams.columns = ['raceId', 'driverId', 'constructorId', 'positionOrder', 'constructorRef']

teams["constructorRef_mapped"] = teams['constructorRef'].map(reversed_constructor_map)

teams = teams.merge(drivers[['driverId', 'driverRef', 'forename', 'surname']], on='driverId', how='left')
teams = teams.merge(races[['year', 'raceId']], on='raceId', how='left')

teams.to_csv(r"data_cleaned\teams.csv", index=False)

# Get the main drivers for each constructor by year:

main_drivers = pd.DataFrame({'race_count': teams.groupby(['year', 'constructorRef_mapped', 'surname'])['raceId']
                            .count()}).sort_values(['constructorRef_mapped', 'year', 'race_count']).reset_index()

# Usually there are two drivers with the odd substitute
main_drivers = main_drivers.groupby(['constructorRef_mapped', 'year'])\
    .apply(lambda x: x.nlargest(2, 'race_count', keep='all')).reset_index(drop=True)

main_drivers.to_csv(r"data_cleaned\main_drivers .csv", index=False)

# Add the mapped constructor ref to the original constructors dataframe

constructors["constructorRef_mapped"] = constructors['constructorRef'].map(reversed_constructor_map)
constructors.to_csv(r"data_cleaned\constructors.csv", index=False)


