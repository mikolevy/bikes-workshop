import csv

import folium
from folium.plugins import MarkerCluster

from bike_service_proxy import BikeServiceProxy

PATH_TO_LOCATIONS = 'locations.csv'
GDANSK_CENTER_POSITION = [54.346320, 18.649246]

bikes_map = folium.Map(location=GDANSK_CENTER_POSITION, zoom_start=10)
markers_cluster = MarkerCluster()
bike_service_proxy = BikeServiceProxy()

with open(PATH_TO_LOCATIONS, mode='r') as locations_file:
    locations_reader = csv.DictReader(locations_file)

    for station_row in locations_reader:

        available_bikes = int(station_row['DOSTĘPNE ROWERY'])
        if available_bikes > 0:

            coordinates_str = station_row['WSPÓŁRZĘDNE']
            coordinates = coordinates_str.split(', ')
            latitude = float(coordinates[0])
            longitude = float(coordinates[1])
            coordinates = [latitude, longitude]

            available_bikes_ids_str = station_row['NUMERY DOSTĘPNYCH ROWERÓW']
            available_bikes_ids = available_bikes_ids_str.split(',')

            for bike_id in available_bikes_ids:

                battery_level = bike_service_proxy.battery_info_for_bike(bike_id)
                if battery_level is None:
                    battery_info = 'Nieznana wartość'
                else:
                    battery_info = f'{battery_level}%'

                bike_info = f'ID: {bike_id} Bateria: {battery_info}'
                bike_marker = folium.Marker(location=coordinates, popup=bike_info)
                markers_cluster.add_child(bike_marker)

bikes_map.add_child(markers_cluster)
bikes_map.save('bikes_map.html')
