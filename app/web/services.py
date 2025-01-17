import requests
import logging
import json
import os

# the default cahce has been set to the memcached docker container
from django.core.cache import cache

logging.root.setLevel('INFO')
logger = logging.getLogger(__name__)



class Weather:

    def __init__(self, zipcode):
        self.zipcode = zipcode

        self.error = None
        self.cachable_data = None

        self.from_cache = None
        self.from_api = None

        self.region = None
        self.temp_f = None
        self.condition = None
        self.wind_mph = None
        self.humidity = None
        self.raw_data_json_string = None

        self.days = []


    def set_data(self, json_string, forecast=False):
        json_string = json_string.replace("\n", "")
        json_string = json_string.replace("\'", "\"")
        self.raw_data_json_string = json_string

        try:
            json_dict = json.loads(json_string)

        except json.JSONDecodeError as error:
            logger.warning(f"Error decoding JSON: {error}")
            self.error = "Error decoding JSON."
            self.error_code = 101
            return False

        try:
            error = json_dict.get('error')
            if error:
                code = error.get('code')
                message = error.get('message')
                self.error = f"Try again! {message}"
                self.cachable_data = True
                return False
                
        except (AttributeError, KeyError) as error:
            logger.warning(f"Malformed JSON string: {error}, json dict is {json_dict}")
            self.error = f"Malformed JSON string"
            self.error_code = 101
            return False
        
        try:
            location = json_dict.get('location')
            current = json_dict.get('current')
            if location:
                self.region = location.get('region')
            if current:
                self.temp_f = current.get('temp_f')
                self.wind_mph = current.get('wind_mph')
                self.humidity = current.get('humidity')
                if current.get('condition'):
                    self.condition = current.get('condition').get('text')
            self.cachable_data = True

        except (AttributeError, KeyError) as error:
            logger.warning(f"Malformed JSON string: {error}, json dict is {json_dict}")
            self.error = f"Malformed JSON string"
            self.error_code = 101
            return False

        if forecast:
            try:
                forecast = json_dict.get('forecast')
                for day in forecast.get('forecastday'):
                    data = { 'date': day.get('date'), 'maxtemp_f': day.get('day').get('maxtemp_f') }
                    self.days.append(data)
                self.cachable_data = True

            except (AttributeError, KeyError) as error:
                logger.warning(f"Malformed JSON string: {error}, json dict is {json_dict}")
                self.error = f"Malformed JSON string"
                self.error_code = 101
                return False

        return True
    

    # returns a dictionary of all the weather vars, when called
    def __call__(self):
        return vars(self)



# accepts a cleaned zipcode from a ZipcodeForm
# returns clean valid dict of vars for template context, of Weather class
def fetch_weather(zipcode, forecast=False):

    weather = Weather(zipcode)

    cache_key = zipcode
    if forecast:
        cache_key = zipcode + "_forecast"

    # cache key should be a str, and value can be any picklable Python object.
    cached_value = cache.get(cache_key)
    

    if cached_value:
        weather.from_cache = True
        weather.set_data(cached_value, forecast=forecast)

    
        # return early
        # Weather class has a self-calling method
        return weather()


    # example data
    """
    bad_response_json_string = '''
        {'error': {
            'code': 1006,
            'message': 'No matching location found.'}}'''

    response_json_string = '''
        {'location': {
            'name': 'New York', 
            'region': 'New York', 
            'country': 'USA', 
            'lat': 40.7643,
            'lon': -73.9874,
            'tz_id': 'America/New_York',
            'localtime_epoch': 1736872685,
            'localtime': '2025-01-14 11:38'},
        'current': {
            'last_updated_epoch': 1736872200,
            'last_updated': '2025-01-14 11:30',
            'temp_c': -1.1,
            'temp_f': 30.0,
            'is_day': 1,
            'condition': {
                'text': 'Sunny',
                'icon': '//cdn.weatherapi.com/weather/64x64/day/113.png',
                'code': 1000},
            'wind_mph': 15.9,
            'wind_kph': 25.6,
            'wind_degree': 298,
            'wind_dir': 'WNW',
            'pressure_mb': 1018.0,
            'pressure_in': 30.07,
            'precip_mm': 0.0,
            'precip_in': 0.0,
            'humidity': 34,
            'cloud': 0,
            'feelslike_c': -7.4,
            'feelslike_f': 18.7,
            'windchill_c': -5.3,
            'windchill_f': 22.5,
            'heatindex_c': 0.1,
            'heatindex_f': 32.2, 'dewpoint_c': -8.0, 'dewpoint_f': 17.6, 'vis_km': 16.0, 'vis_miles': 9.0, 'uv': 1.6, 'gust_mph': 18.7, 'gust_kph': 30.0}}'''
    """




    # if we are over here it means that there was no value in cache so we must grab it from the api

    api_key = os.environ.get('WEATHER_API_KEY')
    if not api_key:
        weather.error = "No API key set in environment variables!"
        return weather()

    api_timeout_secs = 10
    payload = {'key': api_key, 'q': zipcode, 'aqi': 'no'}
    if forecast:
        payload['days'] = "5"

    url = 'http://api.weatherapi.com/v1/current.json'
    if forecast:
        url = 'http://api.weatherapi.com/v1/forecast.json'

    try:
        response = requests.get(url, params=payload, timeout=api_timeout_secs)
    except requests.ConnectTimeout as error:
        weather.error = "connect timeout!"
        return weather()


    # response.url
    # http://api.weatherapi.com/v1/current.json?key=API_KEY_GOES_HERE&q=10019&aqi=no


    # still have to grab the error data from the json string, if these are returned
    '''
    HTTP Status Code    Error code  Description
    401 1002    API key not provided.
    400 1003    Parameter 'q' not provided.
    400 1005    API request url is invalid
    400 1006    No location found matching parameter 'q'
    401 2006    API key provided is invalid
    403 2007    API key has exceeded calls per month quota.
    403 2008    API key has been disabled.
    403 2009    API key does not have access to the resource. Please check pricing page for what is allowed in your API subscription plan.
    400 9000    Json body passed in bulk request is invalid. Please make sure it is valid json with utf-8 encoding.
    400 9001    Json body contains too many locations for bulk request. Please keep it below 50 in a single request.
    400 9999    Internal application error.
    '''
    status_codes_with_json = [200, 400, 401, 403]
    # response.status_code == requests.codes.ok # True
    if response.status_code not in status_codes_with_json:
        weather.error = f"Weather API has an issue! Status code is {response.status_code}."
        return weather()

    # add header checks if I have time
    # header names are case-insensitive
    # response.headers
    # response.headers['Content-Type']   # 'application/json'
    # response.headers.get('content-type')
    
    response_json_string = response.text
    # converts to python dict, raises exception if fails
    # response_json_dict = response.json()

    # todo: add api data validity checks #######
    # bc the data in the api might be bad format, corrupt, etc
    # also dont output the data without sanitizing first,
    # the api could technically xss data in the json 
    # I am not outputting the api data inside of html tags though,
    # so django will escape it for me, but still if I have time I should do this

    # use set_data first, before putting into cache, to catch errors.
    # or else some api error could be added to cache
    weather.set_data(response_json_string, forecast=forecast)
    weather.from_api = True

    # add the data to cache
    # careful to not add invalid data to cache, ever
    if weather.cachable_data:
        cache_timeout_secs = 60 * 60
        cache.set(key=cache_key, value=response_json_string, timeout=cache_timeout_secs)

    # Weather class has a self-calling method
    return weather()