import numpy as np
from scipy import signal

## Moving average filters

def moving_average_lowpass_filter(x, low_cut, sampling_rate):
    filter_length = int(np.ceil(sampling_rate / low_cut))
    b = (np.ones(filter_length)) / filter_length
    return(signal.convolve(x, b, mode='same'))

def moving_average_bandpass_filter(data, low_cut, high_cut, fs):
    nyquist = 0.5 * fs
    low_window = int(fs / low_cut)
    high_window = int(fs / high_cut)
    
    low_kernel = np.ones(low_window) / low_window
    high_kernel = -np.ones(high_window) / high_window
    high_kernel[high_window//2] += 1  
    
    low_pass = np.convolve(data, low_kernel, mode='same')
    high_pass = np.convolve(data, high_kernel, mode='same')
    
    band_pass = high_pass - low_pass
    
    return band_pass

## Apply filters to all channels

def lowpass_every_channel(x, low_cut, sampling_rate):
    return(np.apply_along_axis(moving_average_lowpass_filter, axis=1, arr=x, low_cut=low_cut, sampling_rate=sampling_rate))

def bandpass_every_channel(x, low_cut, high_cut, sampling_rate):
    return(np.apply_along_axis(moving_average_bandpass_filter, axis=1, arr=x, low_cut=low_cut, high_cut=high_cut, fs=sampling_rate))

## LFP functions
    
def capture_LFP(x, sampling_rate):
    return(lowpass_every_channel(x, 300, sampling_rate))

## Brainwave functions

def capture_delta(x, sampling_rate):
    return(bandpass_every_channel(x, 1, 4, sampling_rate))

def capture_theta(x, sampling_rate):
    return(bandpass_every_channel(x, 4, 8, sampling_rate))

def capture_alpha(x, sampling_rate):
    return(bandpass_every_channel(x, 8, 12, sampling_rate))

def capture_beta(x, sampling_rate):
    return(bandpass_every_channel(x, 13, 30, sampling_rate))

def capture_gamma(x, sampling_rate):
    return(bandpass_every_channel(x, 30, 150, sampling_rate))

## Spike functions

def capture_spikes(x, sampling_rate):
    return(bandpass_every_channel(x, 300, 6000, sampling_rate))


