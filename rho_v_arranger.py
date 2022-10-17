import pandas as pd
from tqdm import tqdm
import os
from utils import Utils
import sys

pd.options.mode.chained_assignment = None
n = int(sys.argv[1])

def density_by_velocity(df: pd.DataFrame):
    df['speed'] = df['air_distance'] / df['time_interval']
    # ottengo lista di chi si sposta da terra a mare
    ttm = df.loc[(~ (df['lon_i'] > (-2/3*df['lat_i']+n-10))) & (df['lon_f'] > (-2/3*df['lat_f']+n-10))]

    for lat in tqdm(range(n)):
        for lon in range(n):
            out_df = pd.DataFrame(columns=['r', 'rho'])
            if Utils.is_mare(lat, lon, n) and not ttm.loc[ttm['lat_f'] == lat].loc[ttm['lon_f'] == lon].empty:
                for dist in range(0, df['speed'].max().astype(int), df['speed'].max().astype(int)//100):

                    radius_check = ttm.loc[ttm['speed'] <= dist]

                    num = radius_check.loc[(radius_check['lat_f'] == lat) & (radius_check['lon_f'] == lon)].shape[0]
                    temp = pd.DataFrame({'r': [dist], 'rho': [num]})
                    out_df = pd.concat([out_df, temp], ignore_index=True)
                if (out_df.shape[0] > 0):
                    out_df['rho']
                    out_df.to_csv(f'./speed/{lat}_{lon}.dat', sep='\t', index=False)

if __name__ == '__main__':
    df = Utils.join()
    index = 'speed'

    for i in os.listdir(index):
        os.remove(index+'/'+i)
    density_by_velocity(df)
    Utils.to_non_cum_sum(index = index, n = n)