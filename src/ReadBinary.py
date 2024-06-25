import numpy as np

#reads data from binary file
def read_dataset(raw:str, chan_map_file:str, orientation=-1):
    with open(raw, 'rb') as fid:
        dat = np.fromfile(fid, dtype=np.int16)
        dat = dat.reshape((385, -1), order='F') 
    return dat * orientation

#Generator to create stream of data chunks
def chunk_generator(data, chunk_size):
    num_samples = len(data[0])
    overlap = chunk_size // 20 
    recording_margin = chunk_size // 2
    for start in range(recording_margin, num_samples - recording_margin, chunk_size):
        end = min(start + chunk_size, num_samples)
        start, end = start - overlap, end + overlap
        chunk = [row[start:end] for row in data]
        yield np.array(chunk) 
    



