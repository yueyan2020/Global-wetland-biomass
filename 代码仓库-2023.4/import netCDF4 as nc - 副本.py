import netCDF4 as nc
import pandas as pd
import numpy as np
import xarray as xr
from scipy.interpolate import griddata
file = r'D:\paper\GHG_data\hydro_data\runoff\GRDC-Monthly.nc'
ds = xr.open_dataset('GRDC-Monthly.nc')
df = pd.read_excel('newest_global_river_GHG_321.xlsx')
all_vars=ds.variables.keys()
all_vars_info = ds.variables.items()
print(len(all_vars))
all_vars_info = list(all_vars_info)
print(all_vars_info)
lat = df['Lat'].values
lon = df['Lon'].values
runoff=df['run_off'].values
timeDT = df['Date'].values
var = ds['runoff_mean']
coords = var.coords
points = (lon, lat, timeDT)
dsGeoX = ds['geo_x']
dsGeoY = ds['geo_y']



data2Array = np.stack((dsGeoX.values, dsGeoY.values), axis=1)
keyArr = []
for i in range(len(dsGeoX.values)):
   keyArr = keyArr + [i]

dataArrayIns = xr.DataArray(data2Array, dims=('id', 'xy'), coords={'id': keyArr, 'xy': [0, 1]})

values = []
var2 = (var)
for i in range(len(timeDT)):

    a = np.array([lat[i], lon[i]])
    
    distances = np.linalg.norm(dataArrayIns - a, axis=1)
    index = (np.argmin(distances).flatten()[0])
    index2 = timeDT[i]
    b = index.astype(np.int32)
    value2 = var2.sel(time=index2, method='nearest')
    value = value2.values[index].flatten()
    values.append(value)
lon2 = lon.astype(float)
lat2 = lat.astype(float)
na = runoff.astype(float)

xi = np.array([lon2, lat2, timeDT]).T
mask = pd.isnull(na)

points2 = (lon2, lat2, timeDT)
xi = np.array([lon2, lat2, timeDT]).T


lonlat_time = [(lo, la, t) for lo, la, t in zip(lon2, lat2, timeDT)]
new_lonlat_time = list(set(lonlat_time))

interp_data = griddata(lonlat_time , na, new_lonlat_time, method='nearest')

interp_df = pd.DataFrame({'Lon': [i[0] for i in new_lonlat_time],
                          'Lat': [i[1] for i in new_lonlat_time],
                          'Date': [i[2] for i in new_lonlat_time],
                          'run_off2': interp_data})

df = pd.merge(df, interp_df, on=['Lon', 'Lat', 'Date'], how='outer')
#df['run_off3'] = df['run_off'].fillna(df['run_off2'] )
# df = df.drop(['run_off', 'run_off2'], axis=1)



df.to_excel('newest_global_river_GHG_3212.xlsx', index=False)


# df = pd.read_excel('newest_global_river_GHG_321.xlsx')
# all_vars=ds.variables.keys()
# all_vars_info = ds.variables.items()
# print(len(all_vars))
# all_vars_info = list(all_vars_info)
# print(all_vars_info)
# runoff = ds['runoff_mean']
# times = df['Date'].values
# lons = df['Lon'].values
# lats = df['Lat'].values
# lon = ds['geo_y'].values.tolist()
# lat = ds['geo_x'].values.tolist()
# find_latindex = 26.072
# find_lonindex = 119.568
# lat_index = lat.index(min(lat, key=lambda x: abs(x - find_latindex)))
# lon_index = lon.index(min(lon, key=lambda x: abs(x - find_lonindex)))
# runoff_select = runoff[:, lat_index, lon_index]
# time = ds['time'].values
# df = pd.DataFrame({'time': time, 'runoff_mean': runoff_select})
# df.to_excel('outputnew.xlsx', index=False)
