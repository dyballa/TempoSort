
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