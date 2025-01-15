import requests
import logging
import json

# the default cahce has been set to the memcached docker container
from django.core.cache import cache

logging.root.setLevel('INFO')
logger = logging.getLogger(__name__)


'''
pymemcache.exceptions.MemcacheUnknownCommandError

pymemcache.exceptions.MemcacheClientError

pymemcache.exceptions.MemcacheServerError

pymemcache.exceptions.MemcacheUnknownError

pymemcache.exceptions.MemcacheUnexpectedCloseError

pymemcache.exceptions.MemcacheIllegalInputError

socket.timeout

socket.error
'''


# todo: implement IP address based throttling


class Weather:

    def __init__(self, zipcode):
        self.zipcode = zipcode

        self.error = None

        self.from_cache = None
        self.from_api = None

        self.region = None
        self.temp_f = None
        self.condition = None
        self.wind_mph = None
        self.humidity = None
        self.raw_data_json_string = None

    def set_data(self, json_string):
        json_string = json_string.replace("\n", "")
        json_string = json_string.replace("\'", "\"")
        self.raw_data_json_string = json_string

        try:
            json_dict = json.loads(json_string)

        except json.JSONDecodeError as error:
            logger.warning(f"Error decoding JSON: {error}")
            self.error = "Error decoding JSON."
            return False
        
        try:
            location = json_dict[0].get('location')
            current = json_dict[0].get('current')
            if location:
                self.region = location.get('region')
            if current:
                self.temp_f = current.get('temp_f')
                self.wind_mph = current.get('wind_mph')
                self.humidity = current.get('humidity')
                if current.get('condition'):
                    self.condition = current.get('condition').get('text')

        except AttributeError as error:
            logger.warning(f"Malformed JSON string: {error}, json dict is {json_dict}")
            self.error = f"Malformed JSON string"
            return False

        return True
    

    # returns a dictionary of all the weather vars, when called
    def __call__(self):
        return vars(self)



# accepts a cleaned zipcode from a ZipcodeForm
# returns clean valid dict of vars for template context, of Weather class
def fetch_weather(zipcode):

    weather = Weather(zipcode)

    # cache key should be a str, and value can be any picklable Python object.
    cached_value = cache.get(zipcode)

    if cached_value:
        weather.from_cache = True
        # todo: add cache data validity checks #######
        # bc the data in the cache might be bad format, corrupt, etc
        # also dont output the data without sanitizing first
        weather.set_data(cached_value)
    
        # return early
        # Weather class has a self-calling method
        return weather()





    response_json_string = '''[
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
            'heatindex_f': 32.2, 'dewpoint_c': -8.0, 'dewpoint_f': 17.6, 'vis_km': 16.0, 'vis_miles': 9.0, 'uv': 1.6, 'gust_mph': 18.7, 'gust_kph': 30.0}}]'''


    # if we are over here it means that there was no value in cache so we must grab it from the api
    weather.from_api = True

    ######### todo grab from api


    # todo: add api data validity checks #######
    # bc the data in the api might be bad format, corrupt, etc
    # also dont output the data without sanitizing first,
    # what if the api has xss data in the json lol

    timeout = 60 * 60 # 1 hour

    # cache.set(key, value, timeout=DEFAULT_TIMEOUT, version=None)
    # timeout is in seconds
    cache.set(zipcode, response_json_string, timeout)
    weather.set_data(response_json_string)

    # Weather class has a self-calling method
    return weather()