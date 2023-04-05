import netCDF4 as nc
import pandas as pd
import numpy as np
import xarray as xr
file = r'D:\paper\GHG_data\hydro_data\runoff\GRDC-Monthly.nc'
ds =nc.Dataset(file)
all_vars=ds.variables.keys()
all_vars_info = ds.variables.items()
print(len(all_vars))
all_vars_info = list(all_vars_info)
print(all_vars_info)
df = pd.read_excel('newest_global_river_GHG_321.xlsx')
times = df['Date'].tolist()
lons = df['Lon'].tolist()
lats = df['Lat'].tolist()
find_latindex = 34.968
find_lonindex = 135.99
runoff = ds['runoff_mean'].values
lon = ds['geo_y'].values.tolist()
lat = ds['geo_x'].values.tolist()

values = []
for i in range(len(times)):
    value = var.sel(time=times[i], geo_y=lons[i], geo_x=lats[i], method='nearest').values
    values.append(value)

def extract_value(row):
    time = row['Date']
    lat = row['Lat']
    lon = row['Lon']
    value = ds['runoff_mean'].sel(time=time, geo_x=lat, geo_y=lon, method='nearest').values
    return value
df['run_off'] = df.apply(extract_value, axis=1)
df.to_excel('newest_global_river_GHG_321.xlsx')

times = df['Date'].tolist()
lons = df['Lon'].tolist()
lats = df['Lat'].tolist()
var = ds['runoff_mean']
ds = xr.open_dataset('GRDC-Monthly.nc')
print(ds)
values = []
for i in range(len(times)):
    value = var.sel(time=times[i], geo_y=lons[i], geo_x=lats[i], method='nearest').values
    values.append(value)
df['runoff_mean'] = values
df.to_excel('newest_global_river_GHG_321.xlsx', index=False)