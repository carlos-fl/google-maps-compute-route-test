import requests
from dotenv import load_dotenv
import os


load_dotenv()

def compute_route_matrix(api_key, origins, destinations):
    url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters'
    }

    data = {
    "origin": {
        "location": {
          "latLng": {"latitude": origins['lat'], "longitude": origins['long']}  # Estacion la loarque
        }
    },
    "destination": {
        "location": {
            "latLng": {"latitude": destinations['lat'], "longitude": destinations['long']}  # Estacion la cañada
        }
    },
    "travelMode": "DRIVE",
    "computeAlternativeRoutes": False,
    "routeModifiers": {
      "avoidTolls": False,
      "avoidHighways": False,
      "avoidFerries": False
    },
    "languageCode": "en-US",
    "units": "METRIC"
}

    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        data.get('routes')[0]['duration'] = str(convert_to_minutes(data.get('routes')[0]['duration'])) + ' mins'
        data.get('routes')[0]['distanceMeters'] = str(convert_to_km(data.get('routes')[0]['distanceMeters'])) + ' km'
        return data 
    else:
       'falla' 


def convert_to_minutes(seconds):
    clean_seconds = seconds[:-1]
    minutes = round(int(clean_seconds) / 60, 2)
    return minutes 

def convert_to_km(meters):
    km = round(meters / 1000, 2)
    return km


PLAZA_LOARQUE = {'lat': 14.045584781819803, 'long': -87.21138844012697 }
LA_CANADA = {'lat': 14.04557388333164, 'long':  -87.18617710731718}
print(compute_route_matrix(os.getenv('API_KEY'), PLAZA_LOARQUE, LA_CANADA))

'''
POST REQUEST EXAMPLE
curl -X POST -d '{
  "origin":{
    "location":{
      "latLng":{
        "latitude": 37.419734,
        "longitude": -122.0827784
      }
    }
  },
  "destination":{
    "location":{
      "latLng":{
        "latitude": 37.417670,
        "longitude": -122.079595
      }
    }
  },
  "travelMode": "DRIVE",
  "routingPreference": "TRAFFIC_AWARE",
  "computeAlternativeRoutes": false,
  "routeModifiers": {
    "avoidTolls": false,
    "avoidHighways": false,
    "avoidFerries": false
  },
  "languageCode": "en-US",
  "units": "METRIC"
}' \
-H 'Content-Type: application/json' -H 'X-Goog-Api-Key: YOUR_API_KEY' \
-H 'X-Goog-FieldMask: routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline' \
'https://routes.googleapis.com/directions/v2:computeRoutes'
'''
