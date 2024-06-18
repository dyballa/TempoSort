import numpy as np

def read_dataset(raw : str, chan_map_file: str):
    with open(raw, 'rb') as fid:
        dat = np.fromfile(fid, dtype=np.int16)
        dat = dat.reshape((385, -1), order='F') 

    chan_map = np.load(chan_map_file).ravel()
    dat = dat[chan_map, :]
    return dat


