import numpy as np

#reads data from binary file
def read_dataset(raw:str, chan_map_file:str, orientation=-1):
    with open(raw, 'rb') as fid:
        dat = np.fromfile(fid, dtype=np.int16)
        dat = dat.reshape((385, -1), order='F') 
    return dat * orientation

#Reads next chunk of data from large binary file
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
    
# Get training data with user definied spacing between intervals
def get_training_data(raw_file, training_duration_sec, fs, interval_size_sec=10, dtype=np.int16, sample_size=2, spacing=0):
    
    interval_size = int(fs * min(interval_size_sec, training_duration_sec))
    total_samples = int(training_duration_sec * fs)
    num_intervals = int(np.ceil(total_samples / interval_size))
    interval_sizes = [interval_size for _ in range(num_intervals)]
    interval_sizes[-1] = total_samples - (num_intervals - 1) * interval_size
  
    if num_intervals == 1:
        training_data = next(read_directly_to_chunks(raw_file, chunk_size=total_samples))
        return training_data
  
    traces_list = []
    start_sample = 0
    num_channels = 385
    
    with open(raw_file, 'rb') as fid:
        for i in range(num_intervals):
            fid.seek(start_sample * num_channels * sample_size, 0)
            interval = fid.read(interval_sizes[i] * num_channels * sample_size)
            interval_np = np.frombuffer(interval, dtype=np.int16).reshape((num_channels, -1), order='F') * -1
            traces_list.append(interval_np)
            start_sample += interval_sizes[i] + spacing
    
    traces = np.concatenate(traces_list, axis=1)
    return traces


