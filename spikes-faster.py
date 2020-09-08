'''
7/31
plot histograms of 64 neurons spike trains
	with hard-coded min/max firing rates, preferred direction, tuning curve
	each neuron with PD in each direction
	histogram of each neuron at 0π 
trying to make it faster: num_con=1, num_trial=1, bin=50
missing labels
'''

import numpy as np 
import matplotlib.pyplot as plt 
import math
import signals as sig 
import os

def generate_histograms(num_neurons):
	# constants
	# num_trials = 10
	T = 1000 # trial length (ms)
	bin_width = 50
	r_0 = 35 # (spikes/s)
	r_max = 60
	s = 0
	s_max_array = np.arange(0, 2*np.pi, 2*np.pi/num_neurons)

	num_plot_rows = 8
	num_plot_cols = 8

	plt.figure(figsize=[10, 10])
	
	spike_trains = np.empty(num_neurons, dtype=list)

	# generate spike_trains
	for i in range(num_neurons):
		s_max = s_max_array[i]

		# tuning value
		tuning = r_0 + (r_max-r_0)*np.cos(s-s_max)

		# generate spike trains
		spike_trains[i] = sig.generate_spike_train(T, tuning)

	# plot histograms
	for neuron in range(num_neurons):
		s_max = s_max_array[neuron]

		plt.subplot(num_plot_rows, num_plot_cols, neuron+1)
		plt.title("PD: " + "%.2f"%math.degrees(s_max), fontsize=8)
		plt.tick_params(axis='both', labelbottom=False, labelleft=False)
		plt.ylim([0, r_max*1.5])

		sig.plot_spike_histogram(spike_trains[neuron], T, bin_width)
		plt.tight_layout(pad=0.5)		

		print("neuron " + str(neuron+1) + ": done")

	# save file
	plt.savefig("/Users/taylorchung/Desktop/sImUlAtOr/figs/neurons-64n-1con-minimized.png")
	# plt.show()

generate_histograms(64)
