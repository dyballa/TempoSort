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
#
# #Run MountainSort5
# test_sorting = si.run_sorter(sorter_name='mountainsort5', recording=first_boyden_recording, remove_existing_folder=True, output_folder=output_folder_MS)
#
# #Compare Moutainsort5 to GroundTruth
# GTComp = si.GroundTruthComparison(gt_sorting=first_boyden_sorting, tested_sorting=test_sorting)
#

#matplotlib backend
si.set_default_plotter_backend(backend="ipywidgets")
print(si.get_default_plotter_backend())

from spikeinterface.preprocessing import common_reference

# ipywidgets backend also supports multiple "layers" for plot_traces
recording = first_boyden_recording
rec_dict = dict(filt=recording, cmr=common_reference(recording))
w = si.plot_traces(recording=rec_dict, backend="ipywidgets")