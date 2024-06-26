import matplotlib.pyplot as plt
import numpy as np

#Plot individual channel data
def plot_channel_data(data, channel, begin_interval, end_interval):
    plt.figure()
    extract_ampitudes = data[channel, begin_interval:end_interval]
    times = np.arange(0, len(extract_ampitudes))
    plt.plot(times, extract_ampitudes)
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

# Plot all channels from a dataset
def combined_channel_plot(dataset, begin_interval, end_interval):
    plt.figure(figsize=(10, 6))  # Adjust figsize as needed
    times = np.arange(begin_interval, end_interval)
    num_plots = len(dataset)
    for i in range(dataset):
        plt.plot(times, dataset[i, begin_interval:end_interval] + i * 15)
    plt.show()

def plot_channel_spikes(data, spikes, channel, begin_interval, end_interval):
    plt.figure()
    #overlap  
    extract_ampitudes_filtered = data[channel, begin_interval:end_interval]
    extract_ampitudes_spikes = spikes[channel, begin_interval:end_interval]
    times = np.arange(0, len(extract_ampitudes_spikes))
    plt.plot(times, extract_ampitudes_filtered, label = 'Spikes')
    plt.plot(times, extract_ampitudes_spikes, label='Filtered Data') 
    plt.show()

def plot_sorted_compared_gamma(sorted, gamma, neurons):
    plt.figure()
    times = np.arrange(0, len(sorted))
    #TODO: Add plotting functionality
    plt.plot(times, gamma)
    plt.plot(times, )

