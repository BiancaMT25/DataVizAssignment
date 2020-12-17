import pandas as pd

def wiki_scraper_func(value, url):
    info = []
    for i, link in enumerate(url):
        try:
            df = pd.read_html(link)[0]
            if value in list(df.iloc[:, 0]):
                n = list(df.iloc[:, 0]).index(value)
                info.append(df.iloc[n, 1])
            else:
                df = pd.read_html(link)[1]
                if value in list(df.iloc[:, 0]):
                    n = list(df.iloc[:, 0]).index(value)
                    info.append(df.iloc[n, 1])
                else:
                    df = pd.read_html(link)[2]
                    if value in list(df.iloc[:, 0]):
                        n = list(df.iloc[:, 0]).index(value)
                        info.append(df.iloc[n, 1])
                    else:
                        df = pd.read_html(link)[3]
                        if value in list(df.iloc[:, 0]):
                            n = list(df.iloc[:, 0]).index(value)
                            info.append(df.iloc[n, 1])
        except:
            info.append('not found')

        if len(info) != i + 1:
            info.append("")

    return info


def clean_course_length(df, col_name, col_name_cleaned, new_col_name):
    df[col_name_cleaned] = df[col_name].fillna("not found").apply(lambda x: x.split("km")[0])
    df[col_name_cleaned] = df[col_name_cleaned].apply(lambda x: x.split("mi")[0])
    df[col_name_cleaned] = df[col_name_cleaned].apply(lambda x: x.split("(")[0])
    df[col_name_cleaned] = df[col_name_cleaned].apply(lambda x: x.replace("[1]", ""))
    df[col_name_cleaned] = df[col_name_cleaned].apply(lambda x: x.replace("[2]", ""))
    df[col_name_cleaned] = df[col_name_cleaned].apply(lambda x: x.replace("[3]", ""))
    df[col_name_cleaned] = df[col_name_cleaned].apply(lambda x: x.replace("[4]", ""))
    df[col_name_cleaned] = df[col_name_cleaned].apply(lambda x: x.replace("a", ""))
    df[col_name_cleaned] = df[col_name_cleaned].apply(lambda x: x.replace("\xa0", ""))
    df[new_col_name] = df[col_name_cleaned].apply(pd.to_numeric, errors='coerce')


# load circuit and race data:
circuits = pd.read_csv(r'F1_data\circuits.csv')
races = pd.read_csv(r'F1_data\races.csv')

# get course length for circuits and races:
races['length'] = wiki_scraper_func("Course length", races.url)
circuits['length'] = wiki_scraper_func("Length", circuits.url)
circuits['Turns'] = wiki_scraper_func("Turns", circuits.url)

# clean data:
clean_course_length(circuits, "length", "length_cleaned", "length_val")
clean_course_length(races, "length", "length_cleaned", "length_val")

# fill missing course lengths
races.loc[races.length_val.isnull(), 'length_val'] = [6.940, 4.574, 3.543, 5.554]

# save data:
races.to_csv(r"data_cleaned\races.csv", index=False)
circuits.to_csv(r"data_cleaned\circuits.csv", index=False)

# merge course lengths with lap speed to get km/min:
races = pd.read_csv(r"data_cleaned\races.csv")
circuits = pd.read_csv(r"data_cleaned\circuits.csv")
lap_times = pd.read_csv(r"F1_data\lap_times.csv")

lap_speeds = races[['raceId', 'year', 'length_val']]\
            .merge(right=lap_times[['raceId', 'driverId', 'lap', 'position', 'milliseconds']], on='raceId', how='outer')

lap_speeds['km_per_sec'] = lap_speeds['length_val']/(lap_speeds['milliseconds']*0.001)
lap_speeds['km_per_min'] = lap_speeds['length_val']/((lap_speeds['milliseconds']*0.001)/60)

lap_speeds.dropna(axis=0, inplace=True)

lap_speeds.to_csv(r"data_cleaned\lap_speeds.csv", index=False)



