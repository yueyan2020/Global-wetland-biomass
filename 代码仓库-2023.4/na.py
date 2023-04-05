import netCDF4 as nc
import pandas as pd
import numpy as np
import xarray as xr
import datetime
from scipy.interpolate import griddata
file = r'D:\paper\GHG_data\hydro_data\runoff\GRDC-Monthly.nc'
ds = xr.open_dataset('GRDC-Monthly.nc')

all_vars=ds.variables.keys()
print(len(all_vars))

all_vars_info = ds.variables.items()
all_vars_info = list(all_vars_info)
print(all_vars_info)

start_date = '2020-09-01'
end_date = '2020-09-30'

dsSelected = ds.sel(time=slice(start_date, end_date))
data = dsSelected.variables['runoff_mean'][:]
dataTime = ds.variables['time'][:]

lon_var = dsSelected.variables['geo_y']
lat_var = dsSelected.variables['geo_x']

target_lon = 135.99
target_lat = 34.968

def TryGetLanLonSortedArray(input_lon, input_lat, input_ds):

    # 计算经纬度差值
    lon_diff = np.abs(input_ds.geo_y - input_lon)
    lat_diff = np.abs(input_ds.geo_x - input_lat)
    
    distance = np.sqrt(lon_diff**2 + lat_diff**2)

    lanLonSortedArr = np.argsort(distance)

    return lanLonSortedArr

def TryGetTimeSortedArray(input_time):
    time_diff = np.abs(dataTime.data - input_time)

    # 根据时间差从小到大排序，返回索引
    TimeSortedArr = np.argsort(time_diff)
    return TimeSortedArr

def GetDataByAllParams(input_lon, input_lat, input_time):
    timeArr = TryGetTimeSortedArray(input_time)

    timeLen = len(timeArr)
    for i in range(0, timeLen):
        curTimeIndex = timeArr[i]
        curTime = dataTime.data[curTimeIndex]
        curDs = ds.sel(time=curTime)

        lanLonArr = TryGetLanLonSortedArray(input_lon, input_lat, curDs)
        lanLonLen = len(lanLonArr)
        for i in range(0, lanLonLen):
            curDataIndex = lanLonArr[i]
            returnData = curDs.variables['runoff_mean'].data[curDataIndex]
            if not np.isnan(returnData):
                return returnData
            
    return None




df = pd.read_excel('river_na.xlsx')

lon = df['Lon'].values
lat = df['Lat'].values
time = df['Date'].values

dataLen = len(df)#查看属性lon的长度
data_array = np.zeros(dataLen)#建立一个长度为lon长度的空数据集
for i in range(0, dataLen):
    curLon = lon[i]
    curLat = lat[i]
    curTime = time[i]
    curData = GetDataByAllParams(curLon, curLat, curTime)
    data_array[i] = curData

lon_series = pd.Series(lon, name='Lon')
lat_series = pd.Series(lat, name='Lat')
time_series = pd.Series(time, name='Date')
df = pd.DataFrame({'Lat': lat_series, 'Lon':lon_series , 'DateTime': time_series , 'runOff' : data_array}, index=None)
df.to_excel('na_new.xlsx', index=False)

# lon_idx = np.abs(dsSelected.geo_y - target_lon).argmin().item()
# lat_idx = np.abs(dsSelected.geo_x - target_lat).argmin().item()
# data_var = dsSelected.variables['runoff_mean']
# target_data = data[:, lat_idx, lon_idx]
# lon_lat_time_ds = dsSelected.sel(lon_var=target_lon, lat_var=target_lat, method='nearest')
# lon_index = (abs(lon_var[:] - target_lon)).argmin()
# lat_index = (abs(lat_var[:] - target_lat)).argmin()


# print(data_var)
# data = data_var[:, lat_index, lon_index]
# runoff = ds['runoff_mean'].values #读取气温数据
# lon = ds['geo_y'].values.tolist() #读取经度，并且一定要转化为列表格式，因为后面所使用的函数不支持numpy或者其他格式
# lat = ds['geo_x'].values.tolist() #读取纬度

# #查询距离指定纬度最近的格点


# #读取数据
# runoff_select = runoff[:, lat_idx, lon_idx]
# time = ds['time'].values


# runoff=ds['runoff_mean']
# #target_data = ds.runoff_mean.sel(geo_y=ds.geo_y[lon_idx], geo_x=ds.geo_x[lat_idx], method='nearest').item()
# data_var = ds.variables['runoff_mean']
# data = data_var[:, lat_idx, lon_idx]
# print(data)