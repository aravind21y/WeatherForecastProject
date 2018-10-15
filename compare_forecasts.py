"""This script takes in two city names as input and outputs the differences in
weather between the cities over the next 5 days.

Usage example:

    python compare_forecasts.py Toronto Cleveland

Output example:

    Weather forecast comparison between Toronto and Cleveland:

    Day 1:
    Toronto (18C) will be 3C cooler than Cleveland (21C).
    Toronto will have clear sky, but Cleveland will have rain.

    Day 2:
    Toronto (21C) will be 3C warmer than Cleveland (18C).
    Toronto will have scattered clouds, but Cleveland will have light rain.

    Day 3:
    Toronto and Cleveland will both have the same temperature (20C).
    Toronto and Cleveland will both have light rain.

    Day 4:
    Toronto (18C) will be 3C cooler than Cleveland (21C).
    Toronto and Cleveland will both have light rain.

    Day 5:
    Toronto and Cleveland will both have the same temperature (17C).
    Toronto will have scattered clouds, but Cleveland will have light rain.
"""

import argparse
import requests
import json
import sys

api_url = "http://api.openweathermap.org/data/2.5/forecast/daily?"
api_key = "fe9c5cddb7e01d747b4611c3fc9eaf2c"
number_of_days= 5

def main():
    parser = argparse.ArgumentParser(description="Compare weather forecasts between two cities.")
    parser.add_argument("city1", type=str, help="The first city.")
    parser.add_argument("city2", type=str, help="The second city.")
    args = parser.parse_args()
    #takes the arguments entered from the command line and passes them into the compare_forecast function
    compare_forecasts(args.city1, args.city2)

    #takes the json data format and converts into a dictionary data structure
def json_parse(city):
    city_api = requests.get(api_url + "q=" + city + '&APPID=' + api_key + "&units=metric&cnt=%d" % number_of_days)
    city_data=city_api.json()
    return city_data

def compare_forecasts(city1, city2):
    #calls the json_parse function to parse the json retrieved from the api
    c1data = json_parse(city1) 
    c2data = json_parse(city2)
    
    city_check(c1data,c2data)

    print('')

    print("Weather forecast comparison between {} and {}:".format(city1, city2))

    print('')

    #loops through each day and compares the temperature and weather description between both cities for the number of days specified
    for  i in range(0,len(c1data["list"])):

        c1_temp = int(round(c1data["list"][i]["temp"]["day"]))
        c2_temp = int(round(c2data["list"][i]["temp"]["day"]))
        c1_name = c1data["city"]["name"]
        c2_name = c2data["city"]["name"]
        c1_desc = c1data['list'][i]['weather'][0]['description']
        c2_desc = c2data['list'][i]['weather'][0]['description']
        
        print("Day %d:" % (i+1))
        temp_diff = abs((c1_temp) - (c2_temp))
        
        if c1_temp == c2_temp:
            print(c1_name + " and " + c2_name + " will both have the same temperature (%dC)." % c1_temp)
        elif c1_temp > c2_temp:
            print(c1_name + " (%dC)" % c1_temp +  " will be %dC warmer than " % temp_diff + c2_name + (" (%sC).") % c2_temp)
        else:
            print (c1_name + " (%dC)" % c1_temp +  " will be %dC cooler than " % temp_diff + c2_name + (" (%sC).") % c2_temp)
        
        if  c1_desc != c2_desc:
            print(c1_name + " will have %s," %  c1_desc + " but %s will have " % c2_name + "%s." % c2_desc)
        else:
            print(c1_name + " and " + c2_name + " will both have %s." % c1_desc)    
        print('')
        

    # Validations
def city_check(check1,check2):


    # checks to see if the City name exists
    if (check1["cod"] == "404"):
        sys.exit(check1["message"])
    if (check2["cod"] == "404"):
        sys.exit(check2["message"])

    # if cities are the same ask the user to insert the country code (compares the data in the parsed json object)      
    if check1 == check2:
       sys.exit("These cities have the same name, please specify the country code for both cities e.g London,uk")    
    
if __name__ == "__main__":
     main()

