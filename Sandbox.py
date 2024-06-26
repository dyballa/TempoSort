from src.Detection import*
from src.Filtering import * 
from src.ReadBinary import *
from src.Visualize import * 
from comparisons.Filtering import*
from comparisons.ReadBinary import* 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

sample_data = 'data/2017_rat_hippocampus/decompressed_files'
channel_map = 'data/2017_rat_hippocampus/map_channels' 
channel_locations = 'data/2017_rat_hippocampus/channel_locations'
spike_times = 'data/2017_rat_hippocampus/spike_times'
spike_clusters ='data/2017_rat_hippocampus/spike_clusters' 
fs = 30000

def main(sample_data, channel_map, fs):
    chunked_data = read_directly_to_chunks(sample_data)
    first_chunk = next(chunked_data)
    gamma_comparison(first_chunk, fs, spike_times, spike_clusters)
    # print(np.load(spike_times, mmap_mode="r"))
    # print(np.load(spike_clusters, mmap_mode="r"))
    # timeslice_iterator = timeslice_generator(raw_data, 300)
    # animate_timeslice(raw_data, timeslice_iterator, 1, fs)
 

## Visualize moving average vs. butterworth filtering for LFP 
def compare_avg_butter_LFP(raw_data, fs):
    mv_lfp = capture_LFP(raw_data, fs)
    cmp_lfp = butter_lowpass_filter(raw_data, 300, fs)
    filt_comparison_plot(raw_data, mv_lfp, cmp_lfp, 0, 0, 1000)

## Visualize moving average vs. butterworth highpass filtering 
def compare_avg_butter_compliment(raw_data, fs):
    mv_ap = capture_action_potential(raw_data, fs)
    cmp_ap = raw_data - butter_lowpass_filter(raw_data, 300, fs)
    filt_comparison_plot(raw_data, mv_ap, cmp_ap, 0, 0, 10) 

## Visualize moving average vs. butterworth bandpass filtering
def compare_avg_butter_bandpass(raw_data, fs):
    mv_lfp = capture_action_potential(raw_data, fs)
    cmp_lfp = butter_bandpass_filter(raw_data, 300, 6000, fs)
    filt_comparison_plot(raw_data, mv_lfp, cmp_lfp, 0, 0, 1000) 

## Visualize approximately 20 gamma cycles
def visualize_gammawaves(raw_data,fs):
    samples_per_gamma = fs//40
    twenty_gamma_cycles = samples_per_gamma * 20 
    gamma = capture_gamma(raw_data, fs)
    plot_channel_data(gamma, 0, 0, twenty_gamma_cycles)


def compare_detect_spikes(test_matrix):
    filtered_matrix = butter_bandpass_filter(test_matrix, 300, 6000, fs)
    mv_matrix = capture_action_potential(test_matrix, fs)
    butter_spikes = detect_spikes(filtered_matrix, 20)
    mv_spikes = detect_spikes(mv_matrix, 20)
    plot_channel_spikes(test_matrix, butter_spikes, 1, 0, 5000)
    plot_channel_spikes(test_matrix, mv_spikes, 1, 0, 5000)

## Live plotting of spiking data at Channel 
def animate_timeslice(raw_data, timeslice_iterator, channel, fs):
    fig, ax = plt.subplots()
    x_data, y_data = [], []
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(0, len(raw_data[0]))
    ax.set_ylim(-50, 50)
    timing_array = []

    def update(frame):

        try:
            timeslice = next(timeslice_iterator)
        except StopIteration:
            return line,
        start_time = time.time()
        filtered_timeslice = capture_action_potential(timeslice, fs)
        spikes = detect_spikes(filtered_timeslice, 20)
        end_time = time.time()
        timing_array.append(end_time - start_time)
        channel_spikes = spikes[channel]

       
        x_data.extend(range(len(x_data), len(x_data) + len(timeslice[0])))
        y_data.extend(channel_spikes)

        
        #Displays the last 200ms 
        x_data_disp = x_data[-6000:]
        y_data_disp = y_data[-6000:]
        line.set_data(x_data_disp, y_data_disp)
        ax.set_xlim(max(len(x_data) - 6000, 0), len(x_data))
        ax.set_ylim(np.min(y_data), np.max(y_data))
        return line,

    ani = animation.FuncAnimation(fig, update, blit=True, cache_frame_data=False)
    plt.show()
    # time to process each 10ms timeslice
    print(timing_array)

def param_sweep_filtering(raw_data, fs, gc_spikes):
    detection_threshold = np.sqrt(np.mean(np.array(raw_data)** 2))
    spike_scores = []
    for window in range(30, 500, 20):
        for stride in range(1, 15, 1):
            filtered_data = moving_average_lowpass_filter(raw_data, 300, fs, window_size=window, stride=stride)
            spikes = detect_spikes(filtered_data, detection_threshold)
            score = detection_score(spikes, gc_spikes)
            spike_scores.append(window, stride, score)
    plt.figure()
    window_sizes = spike_scores[:, 0]
    strides = spike_scores[:, 1]
    scores = spike_scores[:, 2]

    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(window_sizes, strides, c=scores, cmap='viridis')

    plt.colorbar(scatter)

    plt.xlabel('Window Size')
    plt.ylabel('Stride')
    plt.title('Accuracy of Spike Detection with Varying Parameters')

    plt.show()

def gamma_comparison(raw_data, fs, spike_times, spike_clusters, start=0, end=7500):

    length_of_interval = end - start

    full_gamma = capture_gamma(raw_data, fs)
    gamma_on_channel = full_gamma[1]
    gamma = gamma_on_channel[start:end]


    spike_cluster_times = format_output(spike_times, spike_clusters)
    
    first_cluster = [time for time in spike_cluster_times[1056]]
    first_cluster_on_interval = [idx for idx in first_cluster if idx < length_of_interval]
    first_cluster_spike_times = np.zeros(length_of_interval)
    first_cluster_spike_times[first_cluster_on_interval] = 50 

    plt.figure()
    times = np.arange(0, length_of_interval)
    plt.plot(times, gamma)
    plt.plot(times, first_cluster_spike_times)
    plt.legend(['Gamma', 'First Cluster'])
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.show()

def format_output(path_to_spike_time, path_to_spike_clusters):
    spike_times = np.load(path_to_spike_time, mmap_mode="r")
    spike_clusters = np.load(path_to_spike_clusters, mmap_mode="r")
    spike_times = spike_times.flatten()
    spike_clusters = spike_clusters.flatten()
    spike_dict = {}
    for i in range(len(spike_times)):
        if spike_clusters[i] in spike_dict:
            spike_dict[spike_clusters[i]].append(spike_times[i])
        else:
            spike_dict[spike_clusters[i]] = [spike_times[i]]
    return spike_dict

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