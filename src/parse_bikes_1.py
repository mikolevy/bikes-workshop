import csv

import folium


PATH_TO_LOCATIONS = 'locations.csv'
GDANSK_CENTER_POSITION = [54.346320, 18.649246]

bikes_map = folium.Map(location=GDANSK_CENTER_POSITION, zoom_start=10)

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
            bike_info = f'{available_bikes} rowerów jest dostępnych'
            bike_marker = folium.Marker(location=coordinates, popup=bike_info)
            bikes_map.add_child(bike_marker)

bikes_map.save('bikes_map.html')
