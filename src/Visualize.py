import matplotlib.pyplot as plt
import numpy as np

def plot_channel_data(data, channel, begin_interval, end_interval):
    plt.figure()
    extract_ampitudes = data[channel, begin_interval:end_interval]
    times = np.arange(0, len(extract_ampitudes))
    plt.plot(times, extract_ampitudes)
    plt.show()

def filt_comparison_plot(raw_data, mv_lfp, cmp_lfp):
    plt.figure()
    raw_data = raw_data[1, :1000]
    mv_lfp = mv_lfp[1, :1000] 
    cmp_lfp = cmp_lfp[ 1, :1000]

    times = np.arange(0, 1000)

    fig, axs = plt.subplots(3, 1, figsize=(8, 6))
    # Subplot 1
    axs[0].plot(times, raw_data)
    axs[0].set_title('Raw Data')

    # Subplot 2
    axs[1].plot(mv_lfp, mv_lfp)
    axs[1].set_title('Moving Average')

    # Subplot 3
    axs[2].plot(times, cmp_lfp)
    axs[2].set_title('Comparison')
    

    plt.show()