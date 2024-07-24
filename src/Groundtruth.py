import numpy as np

#Identify the channels with spikes at given spike times.
def get_channel_spikes_gt(data, spike_times):
    spike_channels = []
    for time in spike_times:
        # Find the channel with the maximum value at the given time
        if(time > len(data[0])):
            break
        while(time = spike_channels[-1][1]):
            time -= 1 
        loc = np.argmax(data[:, time])
        spike_channels.append((loc, time))
    return spike_channels

#Identify any spikes below coorelation 
def identify_subthreshold_gt(data, spike_times): 
    time_radius = 30 #1ms
    spatial_radius = 20 #Arbitrary region 
    coorelation_threshold = .7 # Arbitrary coorelation threshold 

    ch_spikes = get_channel_spikes()
    for channel, time in ch_spikes:
        while index < spatial_radius:
            #Extract times
            template_spike = data[channel, time:time+time_radius]
            compare_values = data[channel+index, time:time+time_radius]

            #Normlize values
            normalized_template = template_spike - np.mean(template_spike) - np.std(template_spike)
            normalized_compare = compare_values - np.mean(compare_values) - np.std(compare_values)

            coorelation = np.coorelate(normalized_template, normalized_compare, "valid") 
            potential_spike_time = np.argmax(coorelation)
            if(potential_spike_time > coorelation_threshold):
                spike_channels.append((loc, time))
    ch_spikes.sort(key=lambda x: x[1])
    return(ch_spikes)



        





    


