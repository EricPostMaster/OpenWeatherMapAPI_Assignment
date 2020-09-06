# OpenWeatherMapAPI_Assignment
This script accesses the OpenWeatherMap API with your API key and pulls a Max/Min 5-day forecast for any city or group of cities you specify.

## Requirements

The guidelines for this assignment were simple:
- Pull 5-day forecasts at 3-hour intervals using the OpenWeatherMap API
- Print the average Min/Max temperatures for each day
- Average the Min temperatures for each day and post that at in a new column
- Average the Max temperatures for each day and post that at in a new column
- Export the result as a CSV file

## Script Process

Here's a quick bulleted list of the script's process:

1. Connected to OpenWeatherMap API to pull weather forecasts in JSON file of 3-hour intervals
1. Used pandas' json_normalize function to flatten the JSON results and create a dataframe
1. Dropped unnecessary columns to keep things clean and simple
1. Calculated Min/Max for each day
1. Calculated average Min/Max for the 5-day range
1. Wrote complete list to CSV and saved it to the same file location as the script

## Learnings

This assignment was the first time I have ever packaged an entire file into a single script.  I still wrote the assignment using cells, but it was rewarding to see it all together in one file at the end.  It was also good because it forced me to keep my code clean throughout the process so I wouldn't forget which parts were essential and which were just for testing.
