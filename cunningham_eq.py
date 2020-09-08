'''
7/29
Test the Cunningham Equation + Linear Algebra
'''

import numpy as np
import matplotlib.pyplot as plt
import math

print("\n\nProgram Start\n\n")

'''
Constants
'''

max_spike_rate = 100
min_spike_rate = 10
max_velocity = 100

'''
Neuron class
'''

class Neuron:

    def __init__(self, num, pd):
        self.num = num
        self.pd = pd

'''
Direction class
'''

class Direction:
    
    def __init__(self, angle):
        self.angle = angle
        self.vector = np.array([round(math.cos(self.angle), 2), round(math.sin(self.angle), 2)])

'''
The eight simple directions of motion
'''

directions = np.array([Direction(0), Direction(math.pi / 4), Direction(math.pi / 2), Direction(math.pi * 3 / 4), Direction(math.pi), Direction(math.pi * 5 / 4), Direction(math.pi * 3 / 2), Direction(math.pi * 7 / 4)])

'''
The eight starting Neurons
'''

neurons = np.array([Neuron(0, directions[0]), Neuron(1, directions[1]), Neuron(2, directions[2]), Neuron(3, directions[3]), Neuron(4, directions[4]), Neuron(5, directions[5]), Neuron(6, directions[6]), Neuron(7, directions[7])])


'''
Cunningham equation function
'''

def spiking_rate(direction, velocity):
    for n in neurons:
        dot_product = direction.vector @ n.pd.vector
        firing_rate = (max_spike_rate - min_spike_rate) * dot_product + min_spike_rate
        print("Neuron " + str(n.num) + " fires at " + str(firing_rate) + " in direction " + str(direction.angle) + " radians.")
        
    
spiking_rate(directions[0], max_spike_rate)
print("\n")
spiking_rate(directions[1], max_spike_rate)
print("\n")
spiking_rate(directions[2], max_spike_rate)
print("\n")
spiking_rate(directions[3], max_spike_rate)
print("\n")
spiking_rate(directions[4], max_spike_rate)
print("\n")
spiking_rate(directions[5], max_spike_rate)
print("\n")
spiking_rate(directions[6], max_spike_rate)
print("\n")
spiking_rate(directions[7], max_spike_rate)
print("\n")

print("\n\nProgram Completed\n\n")
