import h5py as h5
from mma8451.files import dataread

with h5.File('data.h5','r') as f:
    data = dataread(f, "2018", '03', '23', [1,2])

print(data)
