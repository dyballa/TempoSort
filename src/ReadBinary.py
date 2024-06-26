import numpy as np

#reads data from binary file
def read_dataset(raw:str, chan_map_file:str, orientation=-1):
    with open(raw, 'rb') as fid:
        dat = np.fromfile(fid, dtype=np.int16)
        dat = dat.reshape((385, -1), order='F') 
    return dat * orientation

#reads data from large binary file
def read_directly_to_chunks(raw_file, orientation=-1, chunk_size=180000):
    chunked_data = [] 
    
    with open(raw_file, 'rb') as fid:
        num_channels = 385 
        sample_size = np.dtype(np.int16).itemsize 
        
        while True:
            chunk = fid.read(chunk_size * num_channels * sample_size)
            if not chunk:
                break
            chunk_np = np.frombuffer(chunk, dtype=np.int16)
            chunk_np = chunk_np.reshape((num_channels, -1), order='F')
            yield (chunk_np * -1) 

#Generator to create stream of data timeslices
def timeslice_generator(data, timeslice_size):
    num_samples = len(data[0])
    overlap = timeslice_size // 20 
    recording_margin = timeslice_size // 2
    for start in range(recording_margin, num_samples - recording_margin, timeslice_size):
        end = min(start + timeslice_size, num_samples)
        start, end = start - overlap, end + overlap
        timeslice = [row[start:end] for row in data]
        yield np.array(timeslice) 
    



