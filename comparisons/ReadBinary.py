import numpy as np
import spikeinterface as si
import spikeinterface.preprocessing as spre
import spikeinterface.extractors as se

def sp_read_binary(file_path, sampling_frequency, num_channels, dtype):
    recording = si.read_binary(file_paths=file_path, sampling_frequency=sampling_frequency, num_channels=num_channels, dtype=dtype)
    print(recording)
    return(recording)


