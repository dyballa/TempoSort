import numpy as np 
##Schemes for detecting LFP and spikes in the data [NOT DEVELOPED]
##Could use radius as MSort or other methods? Unsure what is best

def detect_LFP(matrix, threshold):
    rows = len(matrix)
    cols = len(matrix[0])
    result_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        max_value = 0 
        for j in range(cols):
            if matrix[i][j] > threshold:
                current_value = matrix[i][j]
                if current_value > max_value:
                    max_value = current_value
                    result_matrix[i][j-1] = 0
                    result_matrix[i][j] = max_value
                else: 
                    max_value = 0 
    return result_matrix

#Thresholding method used to detect spikes
#In the resulting data entries are zeroed if they are not within 30 samples (1 ms) of a peak
def detect_spikes(matrix, threshold):
    rows = len(matrix)
    cols = len(matrix[0])
    result_matrix = np.zeros((rows, cols), dtype=int)

    for i in range(rows):
        counter = 0 
        max_spike = 0
        end_window = 60
        is_spike = False
        while end_window < cols:
           curr = matrix[i, end_window]
           if (counter > 30):
               counter = 0
               result_matrix[i, max_spike_index - 30: max_spike_index + 30] = matrix[i, max_spike_index - 30: max_spike_index + 30]
               is_spike = False
               end_window = max_spike_index + 30
               max_spike = 0
            
           if (curr > threshold):
               is_spike = True
               

           if(is_spike):
               if(max_spike < curr):
                   max_spike = curr
                   max_spike_index = end_window
               end_window += 1 
               counter += 1
           else: 
               end_window += 1
          

    return result_matrix

#Extremely basic detection score (doesn't work well)
def detection_score(spikes, gc_spikes):
    score = 0 
    for i in range(len(spikes[0])):
        for j in range(len(spikes)):
            if (spikes[j][i] > 0) and (gc_spikes[i] != 0):
                score += 100
            elif (spikes[j][i] > 0) and (gc_spikes[i] == 0):
                score -= 1
            elif (spikes[j][i] == 0) and (gc_spikes[i] != 0):
                score -= 40
    return score

#function to calculate rms (used by many algorithms to determine detection threshold)
def calculate_rms(signal):
   return(np.sqrt(np.mean(np.array(signal)** 2)))
