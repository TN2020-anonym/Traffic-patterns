"""
 This file is used to generate examples of underlying road networks in high traffic demand areas.
"""
from pandas import read_csv
import numpy as np
import pickle
import os
import folium
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from matplotlib import rc,rcParams
import warnings
warnings.filterwarnings('ignore')

COORDINATE_CONFIG = {
    'start' : {
        'lat' : 33.588541666667005,
        'lon' : 134.10781250000002
    },
    'offset' : {
        'lat' : 0.0020833333329974835,
        'lon' : 0.003124999999982947
    }
}
RELATIVE_CONFIG = {
    'total_map' : {
        'size' : {
          'h' : 2000,
          'w' : 2000   
        }        
    },
    'studied_map' : {
        'start' : {
            'lat' : 1402,
            'lon' : 163
        },
        'size' : {
            'h' : 100,
            'w' : 250
        }
    }
}

MAP = {
    'center' : [50, 168],
    'boundary' : {
        'zone1' : [ [20, 50],  [20, 100], [80, 100],  [80, 50],   [20, 50]  ],
        'zone2' : [ [40, 100], [40, 180], [100, 180], [100, 100], [40, 100] ],
        'zone3' : [ [20, 180], [20, 250], [80, 250],  [80, 180],  [20, 180] ],
        'total' : [ [18, 74],  [18, 253], [102, 253], [102, 74],  [18, 74]  ]
    }
}

COORDINATE_CONFIG, RELATIVE_CONFIG, MAP

def relativeloc2Coordinate(relative_location, relative_config=RELATIVE_CONFIG, coordinate_config=COORDINATE_CONFIG):
  relativeloc_start = [relative_config['total_map']['size']['h'] - relative_config['studied_map']['start']['lat'], \
                       0 + relative_config['studied_map']['start']['lon']]

  relativeloc = [relativeloc_start[0] - relative_location[0], \
                 relativeloc_start[1] + relative_location[1]]
  
  coordinate = [coordinate_config['start']['lat'] + coordinate_config['offset']['lat']*relativeloc[0], \
                coordinate_config['start']['lon'] + coordinate_config['offset']['lon']*relativeloc[1]]
  
  return coordinate

def pattern2Relativeloc(pattern, lenRelativeloc=3, isSplit=False):
  if isSplit:
    pattern = pattern.split(';')

  locations = []
  for item in pattern:
    y = int(item[-lenRelativeloc:])
    x = int(item[:len(item)-lenRelativeloc])
    location = [x,y]
    locations.append(location)
  return locations

def loc2list(item,lenRelativeloc=3):
  y = int(item[-lenRelativeloc:])
  x = int(item[:len(item)-lenRelativeloc])
  location = [x,y]
  return location

def createBaseMap():
  m = folium.Map(location=relativeloc2Coordinate(MAP['center']), zoom_start=11.5)
  points = [relativeloc2Coordinate(relativeloc) for relativeloc in MAP['boundary']['total']]    
  # folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)
  return m
  
def get_inattentive(patterns):
  inattentive = []
  locations = pattern2Relativeloc(patterns, isSplit=True)
  locations_ = np.array(locations)
  rows = locations_[:, 0]
  cols = locations_[:, 1]
  min_rows, max_rows = rows.min(), rows.max()
  min_cols, max_cols = cols.min(), cols.max()
  
  for i in range(min_rows, max_rows+1):
    for j in range(min_cols, max_cols+1):
      loc = [i, j]
      if loc not in locations:
        inattentive.append(loc)
        
  return inattentive


if __name__ == "__main__":
  # REPLACE YOUR PATTERN HERE TO GENERATE INTERACTIVE MAP OF HIGH TRAFFIC DEMAND REGIONS #
  patterns = '54172;54173;55173;56173;57173;58173;59173;60173;60174;61174;62174;63174;64174;65174' 
  
  inattentive = get_inattentive(patterns)
  locations = patterns.split(';')
  m = createBaseMap()
  for i in range(len(locations)):
    location = locations[i]
    path = './figures/heavy.png'
    img = Image.open(path)
    img.save(path)
    location = loc2list(location)
    folium.raster_layers.ImageOverlay(
      image=path, 
      bounds=[relativeloc2Coordinate(location), relativeloc2Coordinate([x + 1 for x in location])],
      opacity=.3
    ).add_to(m)
      
  m.save('map_road_network.html')

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

