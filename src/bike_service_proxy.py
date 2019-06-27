import io
import json

import requests

LOCATIONS_JS_URL_BASE = 'https://rowermevo.pl/locations.js?key='
LOCATIONS_CSV_URL_BASE = 'https://rowermevo.pl/maps/locations.txt?key='
LOCATIONS_JS_KEY_PATTERN = 'src="/locations.js?key='
LOCATIONS_CSV_KEY_PATTERN = '<a href="/maps/locations.txt?key='
SERVICE_URL = 'https://rowermevo.pl/mapa-stacji/'
HEADERS = {
    'cookie': 'cookies-info=1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


class BikeServiceProxy:

    def __init__(self):
        service_page_content = requests.get(SERVICE_URL, headers=HEADERS).content.decode('utf-8')
        locations_csv_key = self._get_key_to_resource_from_service_page(service_page_content, LOCATIONS_CSV_KEY_PATTERN)
        locations_csv_url = f'{LOCATIONS_CSV_URL_BASE}{locations_csv_key}'
        locations_csv_binary = requests.get(locations_csv_url, headers=HEADERS).content
        self.current_locations_file = io.StringIO(locations_csv_binary.decode('utf-8'))

        locations_js_key = self._get_key_to_resource_from_service_page(service_page_content, LOCATIONS_JS_KEY_PATTERN)
        locations_js_url = f'{LOCATIONS_JS_URL_BASE}{locations_js_key}'

        locations_response = requests.get(locations_js_url, headers=HEADERS)
        batteries_data = self._parse_response_to_batteries_data(locations_response)

        self.parsed_batteries_info = {}
        for bike_data in batteries_data['data']:
            self.parsed_batteries_info[bike_data['bike']] = bike_data['battery']

    def _get_key_to_resource_from_service_page(self, service_page_content, key_pattern):
        src_with_key_index = service_page_content.find(key_pattern)
        key_part_str = service_page_content[src_with_key_index + len(key_pattern):]
        return key_part_str.split('"')[0]

    def _parse_response_to_batteries_data(self, locations_response):
        locations_data = locations_response.content.decode('utf-8')
        batteries_data_line = locations_data.split(';')[1]
        batteries_data_str = batteries_data_line.split("'")[1]
        batteries_data_str = '{"data":' + batteries_data_str + '}'
        return json.loads(batteries_data_str)

    def battery_info_for_bike(self, bike_id):
        return self.parsed_batteries_info.get(bike_id, None)
