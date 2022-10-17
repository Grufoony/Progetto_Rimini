import os
from tqdm import tqdm
import pandas as pd

pd.options.mode.chained_assignment = None

class Utils() :
    @staticmethod
    def is_mare(lat, lon, n):
        return lon > (-2/3*lat+n-10)

    @staticmethod
    def join() -> pd.DataFrame:
        dfs = []
        for i in os.listdir('./output/'):
            dfs.append(pd.read_csv(f'./output/{i}'))
        return pd.concat(dfs, ignore_index=True)

    @staticmethod
    def to_non_cum_sum(index: str, n: int):
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
        final['rho'] = final['rho'] / final['rho'].max()
        final.to_csv(index+'.dat', sep='\t')

    @staticmethod
    def to_cum_sum(index: str, n: int):
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
        final['rho'] = final['rho'].cumsum()
        final['rho'] = 1 - final['rho'] / final['rho'].max()
        final.to_csv(index+'.dat', sep='\t')