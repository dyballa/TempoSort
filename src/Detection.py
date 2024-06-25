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

def detect_spikes(matrix, threshold):
    rows = len(matrix)
    cols = len(matrix[0])
    result_matrix = np.zeros((rows, cols), dtype=int)

    for i in range(rows):
        counter = 0 
        max_spike = 0
        end_window = 40
        is_spike = False
        while end_window < cols:
           curr = matrix[i, end_window]
           if (counter > 20):
               counter = 0
               result_matrix[i, max_spike_index - 20: max_spike_index + 20] = matrix[i, max_spike_index - 20: max_spike_index + 20]
               is_spike = False
               end_window = max_spike_index + 20 
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