# %% [markdown]
# ### BRIa Project - Resting state EEG Analysis 
# 
# Author: Juraj Dedic, xdedic07

# %%
# from scipy.io import loadmat
import mne
from db import engine, Base, load_recoding
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

# %%
Session = sessionmaker(bind=engine)
session = Session()

# %% [markdown]
# ### Download from DB

# %%
ch_names, data_EC = load_recoding(session, 6, tqdm)

data_EC = np.array(data_EC)

# %% [markdown]
# ### Create MNE Raw object

# %%
# print the first 10 values of FP1
print(data_EC[0])
eeg_EC = data_EC * 1e-6 # convert to volts
print(eeg_EC[0])

# create info object
info = mne.create_info(
    ch_names=ch_names,
    ch_types=['eeg']*64, #+ ['eog']*3 + ['misc']*1,
    sfreq=256)

# create raw object
raw = mne.io.RawArray(eeg_EC, info)


montage = mne.channels.make_standard_montage('biosemi64')
# Afz will not be part of ICA
raw.set_channel_types({'Afz': 'misc'})
raw.set_montage(montage)

# %% [markdown]
# ### Initial plot

# %%
# raw.plot(n_channels=20, title="Before", scalings='auto');

# %% [markdown]
# ### Setting reference

# %%
# raw_new_ref = raw.copy()
# raw_new_ref.set_eeg_reference(ref_channels=["Cz"])
# raw_new_ref.plot(n_channels=20, title="Before", scalings='auto');

raw_new_ref = raw.copy()
raw_new_ref.set_eeg_reference(ref_channels="average")
# raw_new_ref.plot(n_channels=20, title="Before", scalings='auto');

# %% [markdown]
# ### Downsampling

# %%
# raw_downsampled = raw.copy().resample(sfreq=200)
# raw_downsampled.plot(n_channels=20, start=10, duration=60, title="After", scalings=dict(eeg=0.05));

# %% [markdown]
# ### Remove low frequency drifts

# %%
# remove slow drifts
raw_straightened = raw_new_ref.copy()
raw_straightened = raw_straightened.filter(l_freq=1.0, h_freq=None)
# raw_straightened.plot(n_channels=32, title="After", scalings=dict(eeg=0.03));

# %%
# raw_tmp = raw_straightened.copy()
# raw_tmp.filter(l_freq=1, h_freq=None)
# ica = mne.preprocessing.ICA(method="picard") 
# fit_params={"extended": True}
# random_state=1
# ica.fit(raw_tmp)

# ica.plot_components(inst=raw_tmp);

# %% [markdown]
# ### Variance explained by ICA components

# %%
# explained_var_ratio = ica.get_explained_variance_ratio(raw_straightened)
# for channel_type, ratio in explained_var_ratio.items():
#     print(
#         f"Fraction of {channel_type} variance explained by all components: " f"{ratio}"
# )

# %%
# def variance_explained_by(i, print_percentage=True):
#     explained_var_ratio = ica.get_explained_variance_ratio(
#         raw_straightened, components=[i], ch_type="eeg"
#     )
#     # This time, print as percentage.
#     if print_percentage:
#         ratio_percent = round(100 * explained_var_ratio["eeg"])
#         print(
#             f"Fraction of variance in EEG signal explained by component "+str(i)+": "
#             f"{ratio_percent}%"
#         )

#     return explained_var_ratio["eeg"]

# variance_explained_by(1, True)


# n = 16
# # plot the variance explained by each component
# variance_explained = []
# for i in range(0, n):
#     variance_explained.append(variance_explained_by(i, False))

# # plot as bar chart with each component on the x-axis labelleds
# plt.figure(figsize=(20, 10))
# plt.bar(range(0, n), variance_explained)
# plt.xlabel("Component")
# plt.ylabel("Fraction of variance explained")
# plt.show();


# %% [markdown]
# ### Plot ICA time series

# %%
# raw.load_data()
# ica.plot_sources(raw, show_scrollbars=False, title="ICA components");

# %% [markdown]
# ## Remove EEG artifacts using ICA

# %%
# ica.exclude = [0,1,2,6,10]
raw_corrected = raw_straightened.copy()

# ica.apply(raw_corrected)
# raw_corrected.plot(n_channels=32, title="After", scalings=dict(eeg=0.02));

# %%


# %% [markdown]
# Feature Extraction for Classification:
# Spectral Features: Band power ratios, dominant
# frequency, spectral entropy.
# Statistical Features: Mean, variance, skewness, kurtosis
# of EEG signals.
# Connectivity Features: Coherence, phase-locking, 
# 
# 5. Connectivity Features:
# Connectivity features reveal the interactions and
# synchronization between different brain regions:
# Coherence: Measures the linear relationship between
# two EEG signals at different frequency bands, indicating
# the degree of synchronization.
# Phase-Locking Value (PLV): Quantifies the phase
# consistency between different EEG channels, reflecting
# functional connectivity.

# %%
epochs = mne.make_fixed_length_epochs(raw=raw_corrected, duration=0.5, overlap=0.25)
times = epochs.times
ch_names = epochs.ch_names

print("calculating connectivity")
# %%
import os.path as op

import mne
from mne_connectivity import spectral_connectivity_epochs
from mne.datasets import sample
from mne_connectivity.viz import plot_sensors_connectivity

# Pick MEG gradiometers
picks = mne.pick_types(
    raw.info, meg=False, eeg=True, stim=False, eog=False
)

# Compute connectivity for band containing the evoked response.
# We exclude the baseline period:
fmin, fmax = 4.0, 9.0
sfreq = raw.info["sfreq"]  # the sampling frequency
tmin = 0.0  # exclude the baseline period
epochs.load_data().pick_types(eeg=True)
con = spectral_connectivity_epochs(
    epochs,
    method="pli",
    mode="multitaper",
    sfreq=sfreq,
    fmin=fmin,
    fmax=fmax,
    faverage=True,
    tmin=tmin,
    mt_adaptive=False,
    n_jobs=1,
)

# Now, visualize the connectivity in 3D:
plot_sensors_connectivity(epochs.info, con.get_data(output="dense")[:, :, 0])


plt.show()

session.close()
print("Done")