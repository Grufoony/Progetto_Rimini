import constants
import pandas as pd
from tqdm import tqdm
import os

pd.options.mode.chained_assignment = None
n = constants.n #numero di celle

def is_mare(lat, lon):
    return lon > (-2/3*lat+n-10)

def join() -> pd.DataFrame:
    dfs = []
    for i in os.listdir('./output/'):
        dfs.append(pd.read_csv(f'./output/{i}'))
    return pd.concat(dfs, ignore_index=True)


def density_by_cell_cum(df: pd.DataFrame):

    # ottengo lista di chi si sposta da terra a mare
    ttm = df.loc[(~ (df['lon_i'] > (-2/3*df['lat_i']+n-10))) & (df['lon_f'] > (-2/3*df['lat_f']+n-10))]


    for lat in tqdm(range(n)):
        for lon in range(n):
            out_df = pd.DataFrame(columns=['r', 'rho'])
            if is_mare(lat, lon) and not ttm.loc[ttm['lat_f'] == lat].loc[ttm['lon_f'] == lon].empty:
                for r in range(n):
                    left_most = lat - r if lat - r >= 0 else 0
                    right_most = lat + r if lat + r <= n-1 else n-1
                    top_most = lon + r if lon + r <= n-1 else n-1
                    bottom_most = lon - r if lon - r >= 0 else 0

                    radius_check = ttm.loc[(ttm['lat_i'] <= right_most) & (ttm['lat_i'] >= left_most) & (ttm['lon_i'] <= top_most) & (ttm['lon_i'] >= bottom_most)]

                    num = radius_check.loc[(radius_check['lat_f'] == lat) & (radius_check['lon_f'] == lon)].shape[0]
                    temp = pd.DataFrame({'r': [r], 'rho': [num]})
                    out_df = pd.concat([out_df, temp], ignore_index=True)
                if (out_df.shape[0] > 0):
                    out_df.to_csv(f'./cells/{lat}_{lon}.dat', sep='\t', index=False)

def density_by_distance(df: pd.DataFrame):
    df['speed'] = df['air_distance'] / df['time_interval']
    # ottengo lista di chi si sposta da terra a mare
    ttm = df.loc[(~ (df['lon_i'] > (-2/3*df['lat_i']+n-10))) & (df['lon_f'] > (-2/3*df['lat_f']+n-10))]

    for lat in tqdm(range(n)):
        for lon in range(n):
            out_df = pd.DataFrame(columns=['r', 'rho'])
            if is_mare(lat, lon) and not ttm.loc[ttm['lat_f'] == lat].loc[ttm['lon_f'] == lon].empty:
                for dist in range(0, df['speed'].max().astype(int), df['speed'].max().astype(int)//100):

                    radius_check = ttm.loc[ttm['speed'] <= dist]

                    num = radius_check.loc[(radius_check['lat_f'] == lat) & (radius_check['lon_f'] == lon)].shape[0]
                    temp = pd.DataFrame({'r': [dist], 'rho': [num]})
                    out_df = pd.concat([out_df, temp], ignore_index=True)
                if (out_df.shape[0] > 0):
                    out_df['rho']
                    out_df.to_csv(f'./speed/{lat}_{lon}.dat', sep='\t', index=False)
                


def to_non_cum_sum(index: str):
    for lat in tqdm(range(n)):
        for lon in range(n):
            if not (os.path.exists(f'./{index}/{lat}_{lon}.dat')):
                continue
            df = pd.read_csv(f'./{index}/{lat}_{lon}.dat', sep='\t')
            eq = df.loc[df['rho'] != df['rho'].shift(1)]
            eq['rho'] = eq['rho'] - eq['rho'].shift(1)
            eq.drop(eq.head(1).index, inplace=True)
            eq['rho'] = eq['rho'].apply(int)
            eq.to_csv(f'./{index}/{lat}_{lon}.dat', sep='\t', index=False)
    final = pd.DataFrame(columns=['r', 'rho'])
    final.set_index('r', inplace=True)
    for lat in tqdm(range(n)):
        for lon in range(n):
            if not (os.path.exists(f'./{index}/{lat}_{lon}.dat')):
                continue
            df = pd.read_csv(f'./{index}/{lat}_{lon}.dat', sep='\t')
            df.set_index('r', inplace=True)
            final = final.add(df, fill_value=0)
    final.to_csv('non_cum_sum.dat', sep='\t')
            

            


# if __name__ == '__main__':
#     import cProfile
#     import pstats

#     with cProfile.Profile() as pr:
#         test()

#     stats = pstats.Stats(pr)
#     stats.sort_stats(pstats.SortKey.TIME)
#     stats.print_stats()
#     stats.dump_stats(filename='stats.dat')
if __name__ == '__main__':
    df = join()
    index = 'speed'
    # for i in os.listdir(index):
    #     os.remove(index+'/'+i)
    # density_by_cell_cum(df)
    # to_non_cum_sum(index = index)

    # for i in os.listdir(index):
    #     os.remove(index+'/'+i)
    # density_by_distance(df)
    # to_non_cum_sum(index = index)

    for i in os.listdir(index):
        os.remove(index+'/'+i)
    density_by_distance(df)
    to_non_cum_sum(index = index)