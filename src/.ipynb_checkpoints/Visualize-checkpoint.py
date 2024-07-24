import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from tkinter import *


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

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

def combined_channel_plot(dataset, chan_map, channel_locs, channels, begin_interval, end_interval):
    import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def combined_channel_plot(dataset, chan_map, channel_locs, channels, begin_interval, end_interval):
    fig, channel_ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(bottom=0.2, right=0.8)

    sample_times = np.arange(begin_interval, end_interval)
    times = sample_times / 30

    # Style subplots
    channel_ax.set_title('Channel Data')
    channel_ax.set_xlabel('Time (ms)')
    channel_ax.set_ylabel('Channel (#)')

    # Position subplot elements
    slider_color = 'White'
    axis_start_channel = plt.axes([0.92, 0.45, 0.03, 0.5], facecolor=slider_color)
    axis_vertical_window = plt.axes([0.85, 0.45, 0.03, 0.5], facecolor=slider_color)
    axis_start_time = plt.axes([0.1, 0.10, 0.65, 0.03], facecolor=slider_color)
    axis_horizontal_window= plt.axes([0.1, 0.06, 0.65, 0.03], facecolor=slider_color)
    neuropixel_ax = fig.add_axes([0.65, 0.04, 0.55, 0.3])

    # Setup logscale for window sliders
    vertical_window_min, vertical_window_max = 1, len(channels)
    log_vertical_window_min, log_vertical_window_max = np.log10(vertical_window_min), np.log10(vertical_window_max)

    # Setup slider ranges
    slider_start_channel = Slider(axis_start_channel, 'Channel', -1, len(channels) - 1, valinit=0, valstep=1, orientation='vertical')
    slider_vertical_window = Slider(axis_vertical_window, 'Window', log_vertical_window_min, log_vertical_window_max, valinit=np.log10(5), valstep=(log_vertical_window_max - log_vertical_window_min) / len(channels), orientation='vertical')
    slider_start_time = Slider(axis_start_time, 'Time', times[0], times[-1], valinit=times[0], orientation='horizontal')
    slider_horizontal_window = Slider(axis_horizontal_window, 'Window', 0, 2, valinit=0, valstep=(np.log10(times[-1]) - np.log10(times[0])) / 100, orientation='horizontal')

    # Represent the zoom slider values using actual values
    def format_vertical_window(val):
        return f'{int(10 ** val)} channels'

    def format_horizontal_window(val):
        return f'{10 ** val:.2f} ms'
    
    slider_vertical_window._format =  format_vertical_window
    slider_horizontal_window._format = format_horizontal_window

    spacing = 25  # Space between channels
    lines = []

    # Graph channel signals
    for i, channel in enumerate(channels):
        line, = channel_ax.plot(times, dataset[channel, begin_interval:end_interval] + i * spacing)
        lines.append(line)

    

    # Update graph view based on slider positions
    def update(val):
        start_channel = int(slider_start_channel.val)
        num_channels = int(10 ** slider_vertical_window.val)  # Convert log scale back to linear scale
        end_channel = min(start_channel + num_channels, len(channels))

        horizontal_window = int(10 ** slider_horizontal_window.val)  # Convert log scale back to linear scale

        channel_ax.set_xlim([slider_start_time.val, slider_start_time.val + horizontal_window])
        channel_ax.set_ylim([start_channel * spacing, end_channel * spacing])

        yticks = range(start_channel * spacing, end_channel * spacing, spacing)
        channel_ax.set_yticks(yticks)
        channel_ax.set_yticklabels(range(start_channel, end_channel))

        for i, line in enumerate(lines):
            line.set_visible(start_channel <= i < end_channel)

        fig.canvas.draw_idle()

        visualize_neuropixel(neuropixel_ax, chan_map, channel_locs, np.arange(start_channel, end_channel), [0])  # TODO: update to call correct function based on class probe type element

    # Call slider update function on slider change
    slider_start_channel.on_changed(update)
    slider_vertical_window.on_changed(update)
    slider_start_time.on_changed(update)
    slider_horizontal_window.on_changed(update)


    

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
def visualize_neuropixel(ax, chan_map, chan_locs, window_channels, selected_channels):
    ax.clear()
    points = zip(chan_locs, chan_map)
    for idx, (loc, value) in enumerate(points):
        x, y = loc
        color = 'black'
        size = 1
        mark = 'o'
        if value in selected_channels: 
            color = 'red'
            ax.text(x + 1, y, str(value), color=color, ha='left', va='center', zorder=2, fontsize=4)
            ax.plot([x, x + 1], [y, y], color=color, linewidth=0.5, zorder=1)
            size = 15
            mark  = 'x'
        elif value in window_channels: 
            color = 'green'
            ax.text(x + 1, y, str(value), color=color, ha='left', va='center', zorder=2, fontsize=4)
            ax.plot([x, x + 1], [y, y], color=color, linewidth=0.5, zorder=1)
            size = 15
            mark = '^'
        ax.scatter(x, y, marker=mark, color=color, s=size, edgecolor='black', zorder=4)
    
    ax.set_aspect(.05)
    ax.set_xlim(0, 65)
    ax.set_ylim(0, 4000)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Neuropixel Channel Map', fontsize=8)
    ax.grid(True)

