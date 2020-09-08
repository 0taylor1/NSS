'''
7/29 2020
generate and plot spike trains
'''

import numpy as np
import matplotlib.pyplot as plt

def generate_spike_train(T, rate):
	'''
	generate spike train given
		trial period (T) in (ms)
		constant firing rate (rate) in (spikes/second)
	'''
	spike_train = np.array(0)
	time = 0

	while time <= T:
		time_next_spike = np.random.exponential(1/rate*1000)
		time += time_next_spike
		spike_train = np.append(spike_train, time)

	if (spike_train[-1] > T):
		spike_train = spike_train[:-1]

	# print("spiketrain", spike_train)
	return spike_train


def generate_spike_train_using_data(times, rates):
	'''
	generate spike train given
		times: array, (ms)
			times in trial period at which data was sampled
		rates: array, (spikes/s)
			time-dependent firing rates from data
	'''
	spike_train = np.array([0])
	while all(spike_train < times[-1]):
		t_prev = spike_train[-1]
		rate_index = 0 if not t_prev else np.where(times<t_prev)[0][-1]
		rate = rates[rate_index]
		t = np.random.exponential(1/rate*1000)
		spike_train = np.append(spike_train, t_prev+t)

	if (spike_train[-1] > times[-1]):
		spike_train = spike_train[:-1]

	# print("spiketrain", spike_train)
	return spike_train

def plot_spike_rasters(S):
	'''
	plot spike rasters given a matrix of spike trains
	borrowed from EE143A hw3 solutions
	'''
	gap = 4
	mark = 5
	pad = 30

	for s in range(np.size(S)):
		spike_train = S[s]
		offset = pad + gap + s*(gap + mark) # offset array

		if np.size(spike_train) != 0:
			spike_train = spike_train[:]

			for t in spike_train.T: # what class instance is train??
				plt.plot([t, t], [offset, offset + mark])

		# plt.xlabel("Time (ms)", fontsize=8)
		plt.ylim([0, offset + mark + gap + pad])


def plot_spike_histogram(S, T, bin_width, num_trials=1):
	'''
	plot spike histogram over all trials over T
		x: time
		y: firing rate
	'''
	i = 0
	start = 0
	stop = start + bin_width
	spike_count = np.array([0])

	while stop <= T:
		spike_count[i] = 0
		for s in S:
			lower_bound = s.compress((s > start).flat)
			upper_bound = s.compress((s < stop).flat)
			spike_count[i] += np.size(np.intersect1d(lower_bound, upper_bound))
		# spike_count[i] = spike_count[i]/(bin_width*pow(10,-3)*num_trials)
		spike_count[i] /= (bin_width*0.001*num_trials)

		# to the next bin
		start += bin_width
		stop += bin_width
		spike_count = np.append(spike_count, 0)
		i += 1

	spike_count = spike_count[: -1] # remove the last 0
	bin_centers = np.arange(bin_width/2, T, bin_width) # start, stop, step
	if len(spike_count != len(bin_centers)):
		print("ERROR")

	print(len(bin_centers))
	print(len(spike_count))
	print(bin_centers)
	print(spike_count)

	plt.bar(bin_centers, spike_count, width=12)

