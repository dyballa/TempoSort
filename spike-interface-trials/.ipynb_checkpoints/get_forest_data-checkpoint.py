import numpy
#Assorted useful python packages
import os
import numpy as np
import tqdm as notebook
import matplotlib.pyplot as plt
from pprint import pprint
import json

import spikeinterface.full as si #all spikeinterface modules
import kachery_cloud as kcl #cloud host for spikeforest datasets
import spikeforest as sf #forked version of spikeforest

current_dir = os.getcwd()


#Note that the order of loaded datasets is NOT the same
all_recordings = sf.load_spikeforest_recordings() #Load all recordings
all_sorting_outputs = sf.load_spikeforest_sorting_outputs() #Load all sortings

#Print details of every recording
for R in all_recordings:
        print('=========================================================')
        print(f'{R.study_set_name}/{R.study_name}/{R.recording_name}')
        print(f'Num. channels: {R.num_channels}')
        print(f'Duration (sec): {R.duration_sec}')
        print(f'Sampling frequency (Hz): {R.sampling_frequency}')
        print(f'Num. true units: {R.num_true_units}')
        print(f'Sorting true object: {json.dumps(R.sorting_true_object)}')
        print('')

#print deatils of every sorting
for X in all_sorting_outputs:
        print('=========================================================')
        print(f'{X.study_name}/{X.recording_name}/{X.sorter_name}')
        print(f'CPU time (sec): {X.cpu_time_sec}')
        print(f'Return code: {X.return_code}')
        print(f'Timed out: {X.timed_out}')
        print(f'Sorting true object: {json.dumps(X.sorting_object)}')
        print('')


#Choose dataset
first_boyden_recording_sf = sf.load_spikeforest_recording(study_name='paired_boyden32c', recording_name='1103_1_1') #, uri='sha1://849e53560c9241c1206a82cfb8718880fc1c6038?paired-boyden-spikeforest-recordings.json')
first_boyden_sorting_sf = sf.load_spikeforest_sorting_output(study_name='paired_boyden32c', recording_name='1103_1_1', sorter_name='JRClust')

#Convert dataset to spikeinterface format
first_boyden_recording = first_boyden_recording_sf.get_recording_extractor()
first_boyden_sorting = first_boyden_sorting_sf.get_sorting_extractor()

print(f'{first_boyden_recording_sf.study_set_name}/{first_boyden_recording_sf.study_name}/{first_boyden_recording_sf.recording_name}')
print(f'{first_boyden_sorting_sf.study_name}/{first_boyden_sorting_sf.recording_name}/{first_boyden_sorting_sf.sorter_name}')

##Set output folder
output_folder_MS = os.path.join(current_dir, 'folder_MS_5')

#Run MountainSort5
test_sorting = si.run_sorter(sorter_name='mountainsort5', recording=first_boyden_recording, remove_existing_folder=True, output_folder=output_folder_MS)

#Compare Moutainsort5 to GroundTruth
GTComp = si.GroundTruthComparison(gt_sorting=first_boyden_sorting, tested_sorting=test_sorting)

