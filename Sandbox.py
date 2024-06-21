from src.Filtering import * 
from src.ReadBinary import *
from src.Visualize import * 
from comparisons.Filtering import*
from comparisons.ReadBinary import* 
import numpy as np
sample_data = 'data/2017_rat_hippocampus/bin_2017'
channel_map = 'data/2017_rat_hippocampus/map_channels' 
channel_locations = 'data/2017_rat_hippocampus/channel_locations'
fs = 30000

def main(sample_data, channel_map, fs):
    raw_data = read_dataset(sample_data, channel_map)
    visualize_gammawaves(raw_data, fs)

## Visualize moving average vs. butterworth filtering for LFP 
def compare_avg_butter_LFP(raw_data, fs):
    mv_lfp = capture_LFP(raw_data, fs)
    cmp_lfp = butter_lowpass_filter(raw_data, 300, fs)
    filt_comparison_plot(raw_data, mv_lfp, cmp_lfp, 0, 0, 1000)

## Visualize moving average vs. butterworth highpass filtering 
def compare_avg_butter_compliment(raw_data, fs):
    mv_lfp = raw_data - capture_LFP(raw_data, fs)
    cmp_lfp = raw_data - butter_lowpass_filter(raw_data, 300, fs)
    print(raw_data[0, 0:10])
    print(mv_lfp[0, 0:10])
    print(cmp_lfp[0, 0:10]) 
    filt_comparison_plot(raw_data, mv_lfp, cmp_lfp, 0, 0, 10) 

## Visualize moving average vs. butterworth bandpass filtering
def compare_avg_butter_bandpass(raw_data, fs):
    mv_lfp = raw_data - capture_LFP(raw_data, fs)
    cmp_lfp = butter_bandpass_filter(raw_data, 300, 6000, fs)
    filt_comparison_plot(raw_data, mv_lfp, cmp_lfp, 0, 0, 1000) 

## Visualize approximately 20 gamma cycles
def visualize_gammawaves(raw_data,fs):
    samples_per_gamma = fs//40 
    twenty_gamma_cycles = samples_per_gamma * 20 
    gamma = capture_gamma(raw_data, fs)
    plot_channel_data(gamma, 0, 0, samples_per_gamma)


##experiments with spike_interface

# def compare_mv_bp_spikes(sample_data, channel_map, fs):
#     raw_data = sp_read_binary(sample_data, fs, 384, "int16")
#     mv_data = mv_trace_flat - capture_LFP(mv_trace_flat, fs)
#     cmp_bp = spikeinterface_bp(cmp_data)
#     cmp_trace = cmp_bp.get_traces(channel_ids=[1], start_frame=0, end_frame=1000)
#     cmp_trace_flat = np.expand_dims(cmp_trace.flatten(), axis=0)
#     filt_comparison_plot(raw_data, mv_trace, cmp_trace_flat, 0, 0, 1000)

## experiments trying to understand channel_locations
#   print(np.load(channel_locations))

if __name__ == "__main__":
    main(sample_data, channel_map, fs)