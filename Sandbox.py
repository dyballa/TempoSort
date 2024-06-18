from scipy.signal import butter
from src.ConvertBenchmarks import *
from src.Visualize import * 
from src.Filtering import * 
from comparisons.Filtering import*


sample_data = 'Benchmarks/2017Demo/Raw/rawDataSample.bin'
channel_map = 'Benchmarks/2017Demo/Raw/channel_map.npy'
fs = 30000

def main(sample_data, channel_map, fs):
    raw_data = read_dataset(sample_data, channel_map)
    #mv_lfp = capture_LFP(raw_data, fs)
    cmp_lfp = comp_LFP(raw_data, fs)
    #filt_comparison_plot(raw_data, mv_lfp, cmp_lfp)
    #plot_channel_data(raw_data, 1, 0, 1000)

if __name__ == "__main__":
    main(sample_data, channel_map, fs)