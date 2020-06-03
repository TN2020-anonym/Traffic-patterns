"""
 This file is used to plot traffic-congested lengths of the specified locations on the map
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


def relativeloc2Coordinate(relative_location, relative_config=RELATIVE_CONFIG, coordinate_config=COORDINATE_CONFIG):
  relativeloc_start = [relative_config['total_map']['size']['h'] - relative_config['studied_map']['start']['lat'], \
                       0 + relative_config['studied_map']['start']['lon']]

  relativeloc = [relativeloc_start[0] - relative_location[0], \
                 relativeloc_start[1] + relative_location[1]]
  
  coordinate = [coordinate_config['start']['lat'] + coordinate_config['offset']['lat']*relativeloc[0], \
                coordinate_config['start']['lon'] + coordinate_config['offset']['lon']*relativeloc[1]]
  
  return coordinate
  
def loc2list(item,lenRelativeloc=3):
  y = int(item[-lenRelativeloc:])
  x = int(item[:len(item)-lenRelativeloc])
  location = [x,y]
  return location

def createBaseMap():
  m = folium.Map(location=relativeloc2Coordinate(MAP['center']), zoom_start=11.5)
  points = [relativeloc2Coordinate(relativeloc) for relativeloc in MAP['boundary']['total']]    
  folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)
  return m

def congested_plot_image(lengths, location, max_y, excluded):
  path = './figures/' + str(location) + '.png'
  x_data = range(len(lengths))
  x_data = [(x+1)*4 for x in x_data]
  y_data = lengths
  
  # activate latex text rendering
  #rc('text', usetex=True)
  rc('axes', linewidth=2)
  rc('font', weight='bold')
  rcParams['text.latex.preamble'] = [r'\usepackage{sfmath} \boldmath']
  
  plt.figure()
  barlist = plt.bar ( x_data, y_data, color='r' )
  print(len(barlist))
  for i in excluded:
    barlist[i].set_color('b')
  plt.xlabel('Timestep (T+i)', fontweight='bold', fontsize='large')
  plt.ylabel('Future congested length (m)', fontweight='bold', fontsize='large')
  plt.ylim((0,max_y))
      
  plt.tight_layout()
  plt.savefig(path, bbox_inches = 'tight', pad_inches = 0.1)
  plt.close()

  return path  

def extract_length(location, start_time, steps, data, offset=400):
  location = int(location)
  lengths = []
  for i in range(steps):
    start_time += offset
    if (start_time % 10000) == 2400:
      start_time -= 2400
      start_time += 10000
    
    try:
        length = data.loc[(data.datetime == start_time) & (data.id == location) & (data.step == 0)]
        length = length.length.values[0]
    except:
        length = 0
    lengths.append(length)
    print(start_time, location, length)
  
  return lengths
  
if __name__ == "__main__":
  # example 1: This is to draw traffic-congested situations for a medium-term pattern
  print('start')
  datasetFile = 'predict_export.csv'
  dataset = pd.read_csv(datasetFile, header=None, index_col=False)
  dataset.columns = ['datetime', 'step', 'x', 'y', 'id', 'length']
  print(dataset.head())
  patterns = '45230;46230;48228;49224;49225;49226;54215;55214;55215'
  start_time = 201507150800
  excluded = [0, 4, 5]
  steps = 6
  locations = patterns.split(';')
  m = createBaseMap()
  for i in range(len(locations)):
    location = locations[i]
    lengths = extract_length(location, start_time-400, steps, dataset, 400)
    path = congested_plot_image(lengths, location, 250, excluded)
    img = Image.open(path)
    img = ImageOps.expand(img,border=2,fill='black')
    img.save(path)
    location = loc2list(location)
    folium.raster_layers.ImageOverlay(
      image=path, 
      bounds=[relativeloc2Coordinate(location), relativeloc2Coordinate([x + 1 for x in location])],
      opacity=.7
    ).add_to(m)
    
  m.save('map_lengths_1.html')
  
  # example 2: This is to draw traffic-congested situations for a long-term pattern
  print('start')
  datasetFile = 'predict_export.csv'
  dataset = pd.read_csv(datasetFile, header=None, index_col=False)
  dataset.columns = ['datetime', 'step', 'x', 'y', 'id', 'length']
  print(dataset.head())
  patterns = '45230;46230;48228;49224;49225;49226;54215;55214;55215'
  start_time = 201507150800
  excluded = []
  steps = 6
  locations = patterns.split(';')
  m = createBaseMap()
  for i in range(len(locations)):
    location = locations[i]
    lengths = extract_length(location, start_time-400, steps, dataset, 400)
    path = congested_plot_image(lengths, location, 250, excluded)
    img = Image.open(path)
    img = ImageOps.expand(img,border=2,fill='black')
    img.save(path)
    location = loc2list(location)
    folium.raster_layers.ImageOverlay(
      image=path, 
      bounds=[relativeloc2Coordinate(location), relativeloc2Coordinate([x + 1 for x in location])],
      opacity=.7
    ).add_to(m)
    
  m.save('map_lengths_2.html')
  
  
  
  
  
  
  

