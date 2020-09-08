'''
7/30
plot histograms of spike trains
	with hard-coded min/max firing rates, preferred direction, tuning curve
	each neuron with PD in each direction
missing labels
'''

import numpy as np
import matplotlib.pyplot as plt
import signals as sig
import os


def generate_histograms(times, angles, num_neurons, num_trials):
	'''	T: times
		S: reach angles '''
	# constants
	T = times[-1] # trial length (ms)
	print(T)
	bin_width = 25
	r_0 = 35 # (spikes/s)
	r_max = 60
	num_cons = 1
	s = angles
	s_max = np.arange(0, 2*np.pi, 2*np.pi/num_neurons) # PD of each neuron
	s_labels = ['0$\pi$',
				'$\pi$/4',
				'$\pi$/2',
				'3$\pi$/4',
				'$\pi$',
				'5$\pi$/4',
				'3$\pi$/2',
				'7$\pi$/4'] # labels for PD of each neurons

	num_plot_rows = num_neurons + 1
	num_plot_cols = num_cons
	plt.figure(figsize=[4, 10])

	# plot reaching angle vs time for reference
	plt.subplot(num_plot_rows, num_plot_cols, 1)
	plt.plot(times, angles)
	# plt.xlabel("time (ms)", fontsize=8)
	# plt.ylabel("reach angle (rad)", fontsize=8)
	plt.tick_params(axis='y', labelsize='small')
	plt.tick_params(axis='x', labelbottom=False, labelleft=False)

	for n in range(num_neurons):
		# tuning curve
		tuning = r_0 + (r_max-r_0)*np.cos(s-s_max[n])

		# generate spike trains
		spike_trains = np.empty((num_neurons, num_trials), dtype=list)
		for trial in range(num_trials):
			spike_trains[n, trial] = sig.generate_spike_train_using_data(times, tuning)

		# plot histograms
		plt.subplot(num_plot_rows, num_plot_cols, (n+2))
		sig.plot_spike_histogram(spike_trains[n,:], T, bin_width, num_trials)
		plt.xlim([0, T])
		plt.ylim([0, r_max*1.5])
		plt.title("PD: " + s_labels[n], fontsize=8)
		plt.tick_params(axis='both', labelbottom=False, labelleft=False)
		print("neuron " + str(n+1) + ": done")

		# plot rasters
		# sig.plot_spike_rasters(spike_trains[n,:])
		# plt.title("PD: " + s_labels[n], fontsize=8)
		# plt.tick_params(axis='both', labelbottom=False, labelleft=False)
		# print("neuron " + str(n+1) + ": done")

	# save file
	plt.tight_layout(pad=0.5)
	plt.savefig('histograms.png')
	# plt.show()

