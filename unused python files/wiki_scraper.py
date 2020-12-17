from CourseLengthScraper import wiki_scraper_func
import pandas as pd

circuits = pd.read_csv(r'F1_data\circuits.csv')
races = pd.read_csv(r'F1_data\races.csv')

races['length'] = wiki_scraper_func("Course length", races.url)
races.to_csv(r"data_cleaned\races.csv", index=False)

circuits['length'] = wiki_scraper_func("Length", circuits.url)
circuits['Turns'] = wiki_scraper_func("Turns", circuits.url)
circuits.to_csv(r"data_cleaned\circuits.csv", index=False)



# Code to scrape wikipedia for weather data from each race
# set up a dictionary to convert weather information into keywords
#weather = races[['raceId', 'url']]
#weather['weather'] = wiki_scraper_func("Weather", races.url)
#
#weather_dict = {'weather_warm': ['soleggiato', 'clear', 'warm', 'hot', 'sunny', 'fine', 'mild', 'sereno'],
#                'weather_cold': ['cold', 'fresh', 'chilly', 'cool'],
#                'weather_dry': ['dry', 'asciutto'],
#                'weather_wet': ['showers', 'wet', 'rain', 'pioggia', 'damp', 'thunderstorms', 'rainy'],
#                'weather_cloudy': ['overcast', 'nuvoloso', 'clouds', 'cloudy', 'grey', 'coperto', 'hazy']}
#
## map new df according to weather dictionary
#
#weather_df = pd.DataFrame(columns=weather_dict.keys())
#for col in weather_df:
#    weather_df[col] = weather['weather'].map(
#        lambda x: 1 if any(i in x.lower() for i in weather_dict[col]) else 0)
#
#weather_info = pd.concat([weather.iloc[:, :3], weather_df], axis=1)
#
#weather_info.to_csv(r"data_cleaned\weather.csv", index=False)