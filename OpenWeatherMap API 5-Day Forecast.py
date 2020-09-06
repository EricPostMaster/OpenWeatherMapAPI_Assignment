# import packages

import pandas as pd
import pprint
import requests
import datetime
import csv


# This is the list of cities I am going to check

loc = [\
        ['Anchorage', 'USA'],\
        ['Buenos Aires', 'Argentina'],\
        ['São José dos Campos', 'Brazil'],\
        ['San José', 'Costa Rica'],\
        ['Nanaimo', 'Canada'],\
        ['Ningbo', 'China'],\
        ['Giza', 'Egypt'],\
        ['Mannheim', 'Germany'],\
        ['Hyderabad', 'India'],\
        ['Tehran', 'Iran'],\
        ['Bishkek', 'Kyrgyzstan'],\
        ['Riga', 'Latvia'],\
        ['Quetta', 'Pakistan'],\
        ['Warsaw', 'Poland'],\
        ['Dhahran', 'Saudia Arabia'],\
        ['Madrid', 'Spain'],\
        ['Oldham', 'England']\
]


complete_list = []  # This will be hold the final product at the end.  It has to be outside the for loop

headers = ['City','Min 1','Max 1','Min 2','Max 2','Min 3','Max 3','Min 4','Max 4','Min 5','Max 5','Min Avg','Max Avg'] # Need to append the headers to the complete_list before adding anything else

complete_list.append(headers)  # Add the headers to the list of temperatures


# This is where the for loop for individual cities begins

k = 0

for city in loc:

    daily_list = []  # This list will start out empty for each city

    city = loc[k][0]
    country = loc[k][1]

    api_key = '{your-API-key}'  # Add your API key here!
    url = 'https://api.openweathermap.org/data/2.5/forecast?'
    url = url + 'q='+ city + ',' + country + '&units=metric&appid=' + api_key

    response = requests.get(url)
    if response.status_code == 200:  # Success
        data = response.json()

    #     printer = pprint.PrettyPrinter(width=80, compact=True)  # This is the part that prints json.
    #     printer.pprint(data['list'][0])                         # Don't need the json for final output.
    else:  # Failure
        print('Error:', response.status_code)

    daily_list.append(str(city + ', ' + country))


    weather = pd.json_normalize(data['list'])  # Put the json data into a dataframe

    # Drop all the columns I don't need
    weather.drop(labels=['dt', 'weather', 'visibility', 'pop', 'main.temp', 'main.feels_like',
                         'main.pressure', 'main.sea_level', 'main.grnd_level', 'main.humidity',
                         'main.temp_kf', 'clouds.all', 'wind.speed', 'wind.deg', 'sys.pod'], axis = 1, inplace=True)

    weather['dt_txt'] = pd.to_datetime(weather['dt_txt'])  # Convert dt_txt column to datetime
    weather['dt_txt'] = weather['dt_txt'].dt.day  # Keep only the day number in the dt_txt column
    weather = weather[weather['dt_txt'] > datetime.datetime.now().day]  # Drop rows for today's date


    # Calculate min and max for each day

    daily_min = weather.groupby(['dt_txt']).min()['main.temp_min']  # Group by date, find minimum in temp_min
    daily_max = weather.groupby(['dt_txt']).max()['main.temp_max']  # Group by date, find maximum in temp_max

    daily_min_max = pd.concat([daily_min, daily_max], axis=1)  # Combine the min and max into a single dataframe
    daily_min_max.reset_index(drop=True, inplace=True)  # Reset index on the dataframe so it can be used in iterations


    # Calculate the average of the minimum and maximum temperatures

    mean_min = round(daily_min_max['main.temp_min'].mean(),2)  # Min
    mean_max = round(daily_min_max['main.temp_max'].mean(),2)  # Max


    # Count unique day values

    num_of_days = weather['dt_txt'].nunique()
    num_of_days

    # Use While loop to pull alternating values from daily_min and daily_max and add them to daily_list

    j = 0

    while j < num_of_days:
        daily_list.append("{:.2f}".format(daily_min_max['main.temp_min'][j]))  # Add min temp for the day as a string
        daily_list.append("{:.2f}".format(daily_min_max['main.temp_max'][j]))  # Add max temp for the day as a string
        j+=1

    daily_list.append("{:.2f}".format(mean_min))  # Add the mean minimum temp for the day (as a string) to the end of the list
    daily_list.append("{:.2f}".format(mean_max))  # Add the mean maximum temp for the day (as a string) to the end of the list
    
    k += 1

    daily_list  # This is a list of the min/max values for each day, as well as the mean min and max
    
    complete_list.append(daily_list)  # Add the city's info to the complete list


# Write the complete_list list to a csv file

file = open('temp.csv', 'w+', newline='')

with file:
    write = csv.writer(file)
    write.writerows(complete_list)