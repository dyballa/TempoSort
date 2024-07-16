import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np


#Plot individual channel data
def plot_channel_data(data, channel, begin_interval, end_interval):
    plt.figure()
    extract_ampitudes = data[channel, begin_interval:end_interval]
    sample_times = np.arange(0, len(extract_ampitudes))
    times = sample_times/30
    plt.plot(times, extract_ampitudes)
    plt.show()
#Plot multple channel data (give channel numbers in array)
def plot_multiple_channels(data, channels, begin_interval, end_interval):
    plt.figure()
    for channel in channels:
        extract_ampitudes = data[channel, begin_interval:end_interval]
        
        #setup x-axis times
        sample_times = np.arange(0, len(extract_ampitudes))
        times = sample_times/30

        plt.plot(times, extract_ampitudes, label=f'Channel {channel}')
    plt.legend()
    plt.show()

# Plot 1 channel from each of 3 datasets
def filt_comparison_plot(raw_data, mv_lfp, cmp_lfp, channel, begin_interval, end_interval):
    plt.figure()

    raw_data = raw_data[channel, begin_interval:end_interval]
    mv_lfp = mv_lfp[channel, begin_interval:end_interval] 
    cmp_lfp = cmp_lfp[channel, begin_interval:end_interval]
   
    #setup x-axis times
    sample_times = np.arange(begin_interval, end_interval)
    times = sample_times/30

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

def combined_channel_plot(dataset, channels, begin_interval, end_interval):
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(bottom=0.2, right=0.8)

    sample_times = np.arange(begin_interval, end_interval)
    times = sample_times / 30

    slider_color = 'White'
    axis_vertical_window = plt.axes([0.92, 0.25, 0.03, 0.65], facecolor=slider_color)
    axis_vertical_zoom = plt.axes([0.85, 0.25, 0.03, 0.65], facecolor=slider_color)
    axis_horizontal_window = plt.axes([0.1, 0.12, 0.65, 0.03], facecolor=slider_color)
    axis_horizontal_zoom = plt.axes([0.1, 0.08, 0.65, 0.03], facecolor=slider_color)

    slider_vertical_window = Slider(axis_vertical_window, 'Channels', -1, len(channels) - 1, valinit=0, valstep=1, orientation='vertical')
    slider_vertical_zoom = Slider(axis_vertical_zoom, 'Zoom', 1, len(channels), valinit=5, valstep=1, orientation='vertical')
    slider_horizontal_window = Slider(axis_horizontal_window, 'Time (ms)', times[0], times[-1], valinit=times[0], orientation='horizontal')
    slider_horizontal_zoom = Slider(axis_horizontal_zoom, 'Zoom', 0, 100, valinit=(times[-1] - times[0]), orientation='horizontal')

    lines = []
    for i, channel in enumerate(channels):
        line, = ax.plot(times, dataset[channel, begin_interval:end_interval] + i * 25)
        lines.append(line)

    def update(val):
        start_channel = int(slider_vertical_window.val)
        num_channels = int(slider_vertical_zoom.val)
        end_channel = min(start_channel + num_channels, len(channels))

        ax.set_xlim([slider_horizontal_window.val, slider_horizontal_window.val + slider_horizontal_zoom.val])
        ax.set_ylim([start_channel * 25, end_channel * 25])

        yticks = range(start_channel * 25, end_channel * 25, 25)
        ax.set_yticks(yticks)
        ax.set_yticklabels(range(start_channel, end_channel))

        for i, line in enumerate(lines):
            line.set_visible(start_channel <= i < end_channel)

        fig.canvas.draw_idle()

    slider_vertical_window.on_changed(update)
    slider_vertical_zoom.on_changed(update)
    slider_horizontal_window.on_changed(update)
    slider_horizontal_zoom.on_changed(update)

    update(None)  # Initial update
    plt.show()


# Plot filtered data from a single channel overlaid with a plot of the detected spikes on that channel
def plot_channel_spikes(data, spikes, channels, begin_interval, end_interval, spike_times=None):
    plt.figure()
    #overlap  
    for channel in channels:
        extract_ampitudes_filtered = data[channel, begin_interval:end_interval]
        extract_ampitudes_spikes = spikes[channel, begin_interval:end_interval]
        sample_times = np.arange(begin_interval, end_interval)
        times = sample_times /30
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
    plt.figure(figsize=(10, 10))
    for idx, (loc, value) in enumerate(zip(chan_locs, chan_map)):
        x, y = loc
        color = 'black'
        if value in channels: 
            color = 'red'
            plt.text(x + 1, y, str(value), color=color, ha='left', va='center', zorder=3, fontsize=10)
            plt.plot([x, x + 1], [y, y], color=color, linewidth=0.5, zorder=1)
        plt.scatter(x, y, color=color, s=15, edgecolor='black', zorder=2)
        
    

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Neuropixel Channel Map')
    plt.grid(True)
    plt.show()