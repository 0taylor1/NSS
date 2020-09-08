'''
8/2 2020
read mouse data from mouse-data.csv
	(timestamp, speed, angle)
use mouse data to generate spike histograms
'''

import numpy as np
import mouse
import spikes2 as sp

num_neurons = 8
num_trials = 100

def load_data():
	# load data
	mouse_times = np.genfromtxt('mouse-data.csv', delimiter=',', dtype=int, usecols=0)
	mouse_speeds = np.genfromtxt('mouse-data.csv', delimiter=',', dtype=float, usecols=1)
	mouse_angles = np.genfromtxt('mouse-data.csv', delimiter=',', dtype=float, usecols=2)

	# discard zeroes
	mouse_times = mouse_times[np.nonzero(mouse_speeds)]
	mouse_speeds = mouse_speeds[np.nonzero(mouse_speeds)]
	mouse_angles = mouse_angles[np.nonzero(mouse_speeds)]

	mouse_times = mouse_times - mouse_times[0]
	return mouse_times, mouse_speeds, mouse_angles

def main():
	mouse.get_mouse_data()
	mouse_times, mouse_speeds, mouse_angles = load_data()
	sp.generate_histograms(mouse_times, mouse_angles, num_neurons, num_trials)
	quit()

main()