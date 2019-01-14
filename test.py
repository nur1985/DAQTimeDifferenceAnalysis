#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pylab

with open("logs/20170124_minerva_minos_daq_time_difference.txt") as f:
    data = f.read()

data = data.split('\n')

x = [row.split(' ')[0] for row in data]
y = [row.split(' ')[1] for row in data]
y2 = [row.split(' ')[2] for row in data]
y3 = [row.split(' ')[3] for row in data]

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Plot title...")    
ax1.set_xlabel('your x label..')
ax1.set_ylabel('your y label...')

ax1.plot(x,y, c='r', label='the data')

leg = ax1.legend()

plt.show()
