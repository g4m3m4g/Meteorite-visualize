'''

import pandas as pd
import numpy as np
import math
from geopy.geocoders import Nominatim

data = pd.read_csv('./meteorite-landings.csv')
data.dropna(inplace = True)

geolocator = Nominatim(user_agent="meteorite_analysis")
def country(coord):
    try:
        location = geolocator.reverse(coord, exactly_one=True, timeout=10) 
        if location:
            address = location.raw['address']
            country_name = address.get('country', '')
            return country_name
        else:
            return "Location not found" 
    except Exception as e: 
        print(f"Error during geocoding for {coord}: {e}")
        return "Geocoding error"
    
lat = data['reclat']
long = data['reclong']

countries = []
is_thailand_list = [] 

for lat, long in zip(lat, long): # Iterate through both Series simultaneously
    coord_str = f"{lat}, {long}" # Create coordinate string
    extracted_country = country(coord_str)
    countries.append(extracted_country)
    is_thailand = extracted_country == "ประเทศไทย"
    is_thailand_list.append(is_thailand)

results_df = pd.DataFrame({'lat': lat, 'long': long, 'country': countries, 'is_thailand': is_thailand_list})
result_df.to_csv('results.csv', index=False)

'''