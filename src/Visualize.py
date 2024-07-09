import matplotlib.pyplot as plt
import numpy as np


#Plot individual channel data
def plot_channel_data(data, channel, begin_interval, end_interval):
    plt.figure()
    extract_ampitudes = data[channel, begin_interval:end_interval]
    times = np.arange(0, len(extract_ampitudes))
    plt.plot(times, extract_ampitudes)
    plt.show()
#Plot multple channel data (give channel numbers in array)
def plot_multiple_channels(data, channels, begin_interval, end_interval):
    plt.figure()
    for channel in channels:
        extract_ampitudes = data[channel, begin_interval:end_interval]
        times = np.arange(0, len(extract_ampitudes))
        plt.plot(times, extract_ampitudes, label=f'Channel {channel}')
    plt.legend()
    plt.show()

# Plot 1 channel from each of 3 datasets
def filt_comparison_plot(raw_data, mv_lfp, cmp_lfp, channel, begin_interval, end_interval):
    plt.figure()
    raw_data = raw_data[channel, begin_interval:end_interval]
    mv_lfp = mv_lfp[channel, begin_interval:end_interval] 
    cmp_lfp = cmp_lfp[channel, begin_interval:end_interval]
    times = np.arange(begin_interval, end_interval)

    fig, axs = plt.subplots(3, 1, figsize=(8, 6))
    # Subplot 1
    axs[0].plot(times, raw_data)
    axs[0].set_title('Raw Data')

    # Subplot 2
    axs[1].plot(times, mv_lfp)
    axs[1].set_title('Moving Average')

    # Subplot 3
    axs[2].plot(times, cmp_lfp)
    axs[2].set_title('Comparison')

    plt.show()

# Plot all channels from dataset on the same graph
deef combined_channel_plot(dataset, channels, begin_interval, end_interval):
    plt.figure(figsize=(10, 6))  # Adjust figsize as needed
    times = np.arange(begin_interval, end_interval)
    num_plots = len(dataset)
    for i, channel in enumerate(channels):
        plt.plot(times, dataset[channel, begin_interval:end_interval] + i * 85)
    plt.show()

# Plot filtered data from a single channel overlaid with a plot of the detected spikes on that channel
def plot_channel_spikes(data, spikes, channels, begin_interval, end_interval, spike_times=None):
    plt.figure()
    #overlap  
    for channel in channels:
        extract_ampitudes_filtered = data[channel, begin_interval:end_interval]
        extract_ampitudes_spikes = spikes[channel, begin_interval:end_interval]
        times = np.arange(begin_interval, end_interval)
        plt.plot(times, extract_ampitudes_filtered, label = 'Spikes{channel}')
        plt.plot(times, extract_ampitudes_spikes, label='Filtered Data{channel}') 
    if spike_times is not None: 
        for x_val in spike_times:
            if begin_interval <= x_val: 
                if(x_val <= end_interval):
                    plt.axvline(x=x_val, color='r', linestyle='--', label=f'GT_Spike={x_val}')
                else:
                    break
    plt.show()

#Function to plot the 1D Fourier transform of the frequencies observed
#Data is a 2D numpy array with any number of channels/rows
def plot_fourier(data, fs, start, end):
    length_of_interval = end - start
    interval = data[start:end]
    fourier = np.fft.fft(interval, axis=1)
    magnitudes = np.abs(fourier)

    plt.figure(figsize=(10, 6))
    for row_magnitudes in magnitudes:
        plt.plot(row_magnitudes)

    plt.title('1D Fourier Transform of Each Row')
    plt.xlabel('Frequency Index')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.grid(True)

    plt.xlim(0, 100)

    plt.show()

#Plot the location of each of the channels in the neuropixel probe
#The parameter channels identifies which channels should be plotted in red
def visualize_neuropixel(chan_map, chan_locs, channels):
    print(chan_locs)
    plt.figure(figsize=(10, 10))
    for idx, (loc, value) in enumerate(zip(chan_locs, chan_map)):
        x, y = loc
        color = 'red' if value in channels else 'black'
        plt.scatter(x, y, color=color, s=100, edgecolor='black', zorder=2)
        plt.text(x, y, str(value), color='white', ha='center', va='center', zorder=3)
    
    # plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Neuropixel Channel Map')
    plt.grid(True)
    plt.show() 
