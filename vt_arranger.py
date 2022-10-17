import pandas as pd
from tqdm import tqdm
import os
from utils import Utils
import sys

pd.options.mode.chained_assignment = None
n = int(sys.argv[1])

dt = int(sys.argv[2]) #step for distance

def density_by_distance(df: pd.DataFrame):
    # ottengo lista di chi si sposta da terra a mare
    ttm = df.loc[(~ (df['lon_i'] > (-2/3*df['lat_i']+n-10))) & (df['lon_f'] > (-2/3*df['lat_f']+n-10))]

    out_df = pd.DataFrame(columns=['r', 'v'])

    for delta in range(0, ttm['real_distance'].max().astype(int), ttm['real_distance'].max().astype(int)//dt):

        radius_check = ttm.loc[(ttm['real_distance'] <= delta) & (ttm['real_distance'] > delta-dt)]
        mean = (radius_check['real_distance']/radius_check['time_interval']).mean()
        temp = pd.DataFrame({'r': [delta], 'v': [mean]})
        out_df = pd.concat([out_df, temp], ignore_index=True)
    out_df.to_csv(f'./vt.dat', sep='\t', index=False)

if __name__ == '__main__':
    df = Utils.join()
    index = 'vt'
    density_by_distance(df)