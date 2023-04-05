
import numpy as np
from scipy.interpolate import interp1d

# 缺失值用 NaN 表示
data = np.array([1, 2, np.nan, 4, 5])

# 构造插值函数
f = interp1d(np.arange(len(data)), data, kind='nearest', fill_value='extrapolate')

# 对缺失值进行插值
new_data = f(np.arange(len(data)))

print(new_data)