import tweepy, time, requests, json, datetime, string
from credentials import * #Imports hidden credentials/API keys from a credentials.py

#API responds in Kelvin, convert Kelvin forecast temperature to Fahrenheit
def convert_temp(kelvin_temp):
    fahrenheit_temp = 9/5*(kelvin_temp - 273) + 32
    return fahrenheit_temp

#Formats forecast time into easily readable words
def format_forecast_time(forecast_time):
    date = forecast_time.split()[0]
    if int(date.split('-')[1]) == 1:
        date_in_words = 'January ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 2:
        date_in_words = 'February ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 3:
        date_in_words = 'March ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 4:
        date_in_words = 'April ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 5:
        date_in_words = 'May ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 6:
        date_in_words = 'June ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 7:
        date_in_words = 'July ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 8:
        date_in_words = 'August ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 9:
        date_in_words = 'September ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 10:
        date_in_words = 'October ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 11:
        date_in_words = 'November ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    elif int(date.split('-')[1]) == 12:
        date_in_words = 'December ' + date.split('-')[2] + ', ' + date.split('-')[0] + ' ' + forecast_time.split()[1]
    return date_in_words

#Figures out what advice to put in the tweet
def get_advice(weather_category):
    rain = {'Thunderstorm', 'Drizzle', 'Rain'}
    if weather_category in rain:
        advice = 'Bring an umbrella!'
    elif weather_category == 'Snow':
        advice = 'Wear boots!'
    elif weather_category == 'Atmosphere':
        advice = 'Be careful driving!'
    elif weather_category == 'Clear':
        advice = 'Bring water!'
    elif weather_category == 'Clouds':
        advice = 'Wear a jacket!'
    elif weather_category == 'Extreme':
        advice = 'Extreme weather alert!!'
    elif weather_category == 'Additional':
        advice = 'It\'s windy out there!'
    return advice

def get_forecast_message():
    #Calling openweathermap API for the weather forecast data in JSON of East Brunswick restricted to 24 hours in the future
    forecast_payload = {'id': '5097402', 'cnt': '8', 'appid': apikey}
    forecast_request = requests.get('http://api.openweathermap.org/data/2.5/forecast?', params = forecast_payload)
    forecast = json.loads(forecast_request.text)

    #Gets necessary weather forecast data for tweet from API request
    city = forecast['city']['name']
    forecast_unix_time = forecast['list'][0]['dt']
    forecast_time = datetime.datetime.fromtimestamp(int(forecast_unix_time)).strftime('%Y-%m-%d %H:%M:%S') #Converting from Unix time to slightly more readable format
    formatted_forecast_time = format_forecast_time(forecast_time)
    weather = string.capwords(forecast['list'][0]['weather'][0]['description'])
    high_temp = float(convert_temp(forecast['list'][0]['main']['temp_max']))
    low_temp = float(convert_temp(forecast['list'][0]['main']['temp_min']))
    average_temp = float((high_temp + low_temp) / 2)
    weather_category = forecast['list'][0]['weather'][0]['main']
    advice = get_advice(weather_category)

    #Concatenates all the weather data into a forecast message
    message = '{} {}\n{}\nHigh: {}° F\nLow: {}° F\nAvg: {}° F\n{}\nno tweet=unchanged'.format(city, formatted_forecast_time, weather, high_temp, low_temp, average_temp, advice)
    return message

def tweet():
    try: #Handles exceptions where the forecast has not changed from last tweet and Tweepy gives 'Status is a duplicate.' error
        tweet = get_forecast_message() #Call function to get the weather forecast message to tweet
        print(tweet) #Debugging purposes
        api.update_status(tweet) #Tweets
        time.sleep(3600) #Wait one hour before tweeting again
    except tweepy.TweepError as e:
        print(e.reason)
        time.sleep(3600) #Wait one hour before tweeting again if it's a 'Status is duplicate.' error

#Access twitter account to be able to tweet from it
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Bot tweets indefinitely until process is stopped
while True:
    tweet()