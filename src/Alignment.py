from Detection.py import detect_LFP

def align_spikes(filtered_data, lfp_array):
    aligned_matrix = detect_LFP(lfp_array, 3)