from kilosort import run_kilosort, DEFAULT_SETTINGS

def default_kilosort(probe_name):
    settings = DEFAULT_SETTINGS
    settings['n_chan_bin'] = 385
    settings['data_dir'] = '/data/'
    ops, st, clu, tF, Wall, similar_templates, is_ref, est_contam_rate = run_kilosort(settings=settings, probe_name='data/map_channels')

