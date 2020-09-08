'''
7/29
plot the first 8 neurons
	with hard-coded min/max firing rates, preferred direction, tuning curve
	each neuron with PD in each dirrection (see line 18)
haha it works?! :)))
'''

import numpy as np 
import matplotlib.pyplot as plt 
import signals as sig 
import os

# constants
num_trials = 100
T = 1000 # trial length (ms)
bin_width = 20
r_0 = 35 # (spikes/s)
r_max = 60
num_cons = 1
num_neurons = 1
s = np.arange(num_cons)*np.pi/4 # (radians)
s_max = np.arange(num_cons)*np.pi/4 
s_labels = ['0$\pi$', '$\pi$/4', '$\pi$/2', '3$\pi$/4', '$\pi$', '5$\pi$/4', '3$\pi$/2', '7$\pi$/4']

for i in range(num_neurons):
	# tuning curve
	tuning = r_0 + (r_max-r_0)*np.cos(s-s_max[i])

	# generate spike trains
	spike_trains = np.empty((num_cons, num_trials), dtype=list)
	for con in range(num_cons):
		for trial in range(num_trials):
			spike_trains[con, trial] = sig.generate_spike_train(T, tuning[con])


	# plot spike rasters and histograms
	num_rasters = 5
	num_plot_rows = 8
	num_plot_cols = 2

	plt.figure(figsize=[8, 10])

	for con in range(num_cons):
		# spike raster
	    plt.subplot(num_plot_rows, num_plot_cols, num_plot_cols*con+1)
	    sig.plot_spike_rasters(spike_trains[con, 0:num_rasters])
	    plt.title(s_labels[con] + ' radians', fontsize=12, loc='left')
	    plt.tick_params(labelsize=8)
	    plt.tight_layout(pad=0.5)

	    # spike histogram
	    plt.subplot(num_plot_rows, num_plot_cols, num_plot_cols*con+2)
	    sig.plot_spike_histogram(spike_trains[con,:], T, bin_width, num_trials)
	    plt.xlim([0, T])
	    plt.ylim([0, 100])
	    plt.tick_params(labelsize=8)
	    plt.tight_layout(pad=0.5)

	plt.suptitle("Neuron " + str(i) + ", PD: " + str(s_labels[i]), fontsize='16')
	plt.subplots_adjust(top=0.94)

	# save file
	plt.savefig("/Users/taylorchung/Desktop/sImUlAtOr/f" + str(i+1) + ".png")
	# plt.show()
