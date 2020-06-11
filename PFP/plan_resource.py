"""
 This file is used to plot traffic-congested lengths of the specified locations on the map
"""
from map_utils import *
  
if __name__ == "__main__":
  datasetFile = '../Fusion_3DCNN/predict_export.csv'
  dataset = pd.read_csv(datasetFile, header=None, index_col=False)
  dataset.columns = ['datetime', 'step', 'x', 'y', 'id', 'length']
  
  # example 1: This is to draw traffic-congested situations for a medium-term pattern
  print('start example 1')  
  patterns = '29083;74100;76101;76102;77102;79104;89141'
  timestamps = [201507052000, 201507060000, 201507060400, 201507060800, 201507061200, 201507061600]
  excluded = [0,4,5]
  locations = patterns.split(';')
  m = createBaseMap()
  for i in range(len(locations)):
    location = locations[i]
    lengths = extract_length(location, timestamps, dataset)
    path = congested_plot_image(lengths, location, 400, excluded)
    print(path)
    img = Image.open(path)
    img = ImageOps.expand(img,border=2,fill='black')
    img.save(path)
    location = loc2list(location)
    folium.raster_layers.ImageOverlay(
      image=path, 
      bounds=[relativeloc2Coordinate(location), relativeloc2Coordinate([x + 1 for x in location])],
      opacity=.7
    ).add_to(m)
    
  m.save('results/plan_resources_1.html')
  
  # example 2: This is to draw traffic-congested situations for a long-term pattern
  print('start example 2')  
  patterns = '97146;98145;97145'
  timestamps = [201508220400, 201508220800, 201508221200, 201508221600, 201508222000, 201508230000]
  excluded = []
  locations = patterns.split(';')
  m = createBaseMap()
  for i in range(len(locations)):
    location = locations[i]
    lengths = extract_length(location, timestamps, dataset)
    path = congested_plot_image(lengths, location, 520, excluded)
    print(path)
    img = Image.open(path)
    img = ImageOps.expand(img,border=2,fill='black')
    img.save(path)
    location = loc2list(location)
    folium.raster_layers.ImageOverlay(
      image=path, 
      bounds=[relativeloc2Coordinate(location), relativeloc2Coordinate([x + 1 for x in location])],
      opacity=.7
    ).add_to(m)
    
  m.save('results/plan_resources_2.html')
  
  
  
  
  
  
  

