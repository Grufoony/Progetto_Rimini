import pandas as pd
import numpy as np
import math
import sys
import os
from tqdm import tqdm

r = 6371000 # meters

df = pd.read_csv('./data/rimini_20200810_activity.csv', sep = ';')

lat_max = df['lat'].max()
lat_min = df['lat'].min()
lon_max = df['lon'].max()
lon_min = df['lon'].min()
phi_0 = (lon_max + lon_min) / 2

x1 = r * math.radians(lat_max) * math.cos(math.radians(phi_0))
y1 = r * math.radians(lon_max)
x2 = r * math.radians(lat_min) * math.cos(math.radians(phi_0))
y2 = r * math.radians(lon_min)
cart_dis = math.sqrt((x1-x2)**2 + (y1-y2)**2)

side = cart_dis / math.sqrt(2)
grid_side = side / 380
grid_size = grid_side**2
print(grid_side)
print(grid_size)