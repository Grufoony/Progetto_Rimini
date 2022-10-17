import pandas as pd
import numpy as np
import math
import sys
import os
from tqdm import tqdm

n = int(sys.argv[1]) #numero di celle da creare

r = 6371000 # meters

def sort(name: str):
    # creo automaticamente il database con pandas
    df = pd.read_csv('./data/'+name, sep = ';')
    # #id_act - lat - long - timestamps

    out = pd.DataFrame()

    #ids column
    ids=df['id_act'].unique()
    out['id_act']=ids

    #cells
    lat_max = df['lat'].max()
    lat_min = df['lat'].min()
    lon_max = df['lon'].max()
    lon_min = df['lon'].min()
    dlat = abs(lat_max - lat_min)/n
    dlon = abs(lon_max - lon_min)/n

    id_lat = df.groupby(['id_act'])['lat'].agg(['first','last'])
    id_lat = (abs(id_lat-lat_min)/dlat).apply(np.floor)

    id_lon = df.groupby(['id_act'])['lon'].agg(['first','last'])
    id_lon = (abs(id_lon-lon_min)/dlon).apply(np.floor)

    # #time max and min
    time_max=df.groupby(['id_act'])['timestamp'].max()
    time_min=df.groupby(['id_act'])['timestamp'].min()
    time = []
    lat_f = []
    lon_f = []
    lat_l = []
    lon_l = []

    #distance 
    for id in tqdm(ids):
        lat_f.append(int(id_lat.loc[[id]]['first'][id]))
        lon_f.append(int(id_lon.loc[[id]]['first'][id]))
        lat_l.append(int(id_lat.loc[[id]]['last'][id]))
        lon_l.append(int(id_lon.loc[[id]]['last'][id]))
        user_data = df.loc[df['id_act'] == id] # ottengo tutti i dati per quell'id
        max_lat = pd.to_numeric(user_data['lat'].max())
        max_lon = pd.to_numeric(user_data['lon'].max())
        min_lat = pd.to_numeric(user_data['lat'].min())
        min_lon = pd.to_numeric(user_data['lon'].min())
        phi_0 = (max_lon + min_lon) / 2
        lat = user_data['lat'].tolist()
        lon = user_data['lon'].tolist()
        i = 0
        tot_distance = 0
        length = len(lat) - 1
        while i < length:
            x1 = r * math.radians(lat[i]) * math.cos(math.radians(phi_0))
            y1 = r * math.radians(lon[i])
            x2 = r * math.radians(lat[i+1]) * math.cos(math.radians(phi_0))
            y2 = r * math.radians(lon[i+1])
            cart_dis = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            tot_distance += cart_dis
            i += 1
        out.loc[out['id_act'] == id, 'real_distance'] = tot_distance

        #air distance
        x1 = r * math.radians(max_lat) * math.cos(math.radians(phi_0))
        y1 = r * math.radians(max_lon)
        x2 = r * math.radians(min_lat) * math.cos(math.radians(phi_0))
        y2 = r * math.radians(min_lon)
        tot_distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        out.loc[out['id_act'] == id, 'air_distance'] = tot_distance
        
        #time array addition
        time.append(time_max[id]-time_min[id])

    out.insert(loc=1, column='lat_i', value=lat_f)
    out.insert(loc=2, column='lon_i', value=lon_f)
    out.insert(loc=3, column='lat_f', value=lat_l)
    out.insert(loc=4, column='lon_f', value=lon_l)
    out.insert(loc=5, column='time_interval', value=time)

    out.to_csv('output/' + name.split('.')[0] + '_output.csv', index=False)

if __name__ == '__main__':
    for i in os.listdir('data'):
        sort(i)