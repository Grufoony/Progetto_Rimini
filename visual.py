import geopandas as gpd
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
from PIL import Image
import sys

from tqdm import tqdm

n = int(sys.argv[1])

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

df = pd.read_csv(sys.argv[2])
id = sys.argv[2].split('_')[1]
# print(df.head())

tot = df['id_act'].size

init_visits = np.zeros((n+1, n+1))
final_visits = np.zeros((n+1, n+1))
for i in tqdm(df.index):
    lat = int(df.loc[i].lat_i)
    lon = int(df.loc[i].lon_i)
    init_visits[n-lat][lon] = init_visits[n-lat][lon] + 1
    lat = int(df.loc[i].lat_f)
    lon = int(df.loc[i].lon_f)
    final_visits[n-lat][lon] = final_visits[n-lat][lon] + 1
init_visits = init_visits / tot
final_visits = final_visits / tot

#initial density plot
init_im = plt.imshow(init_visits, cmap="gnuplot2")
plt.colorbar(init_im)
plt.savefig('./img/' + id + '_init.png')
plt.close()

#final density plot

final_im = plt.imshow(final_visits, cmap="gnuplot2")
plt.colorbar(final_im)
plt.savefig('./img/' + id + '_final.png')
plt.close()

# #shapefile plot
# shape = gpd.read_file('./rimini/output_areas.shp')
# axes = shape.plot()
# fig = axes.get_figure()
# fig.savefig("./img/city.png")

# map = Image.open(r"./map.png")
# city = Image.open(r"./city.png")
# print(map.size)
# print(city.size)
# city.paste(map, (0,0))
# city.save("./prova.png")

# map = Image.open('./map.png')
# map = map.convert("RGBA")
# datas = map.getdata()

# newData = []
# for item in datas:
#     if item[0] == 255 and item[1] == 255 and item[2] == 255:
#         newData.append((255, 255, 255, 0))
#     else:
#         newData.append(item)

# map.putdata(newData)

# city = Image.open("./city.png")
# city = city.convert("RGBA")
# datas = city.getdata()

# newData = []
# for item in datas:
#     if item[0] == 255 and item[1] == 255 and item[2] == 255:
#         newData.append((255, 255, 255, 0))
#     else:
#         newData.append(item)

# city.putdata(newData)


# map.putalpha(120)
# city.putalpha(120)
# city = city.rotate(-5, expand = 1)
# city.paste(map, (0,15), map)
# city.save("./prova.png")