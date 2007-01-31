#!/usr/bin/env python
#------------------------------------------------------------------------------
# Copyright (c) 2006-2007 Nicolas Rougier.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
# 
# $Id$
#------------------------------------------------------------------------------

import matplotlib.pylab as pylab
import matplotlib.colors as colors

import dana.core as core
import dana.projection as proj
import dana.cnft as cnft
import dana.learn as learn
import dana.view as view
import dana.projection as projection
import dana.projection.distance as distance
import dana.projection.density as density
import dana.projection.shape as shape
import dana.projection.profile as profile
import time, random, math
import gobject, gtk
import numpy
import random


#   The purpose of this model is to classify odd and even numbers, using the 
#   perceptron algorithm 
#
#   The numbers are represented with 7 segments
#                  1
#              ---------
#             6|       | 2
#              |   7   |
#              ---------
#             5|       | 3
#              |       |
#              ---------
#                  4
#                  
#  Then, 0 is represented by (1111110)
#        1 is represented by (0110000)
#        2 is represented by (1101101)
#        3 is represented by (1111001)
#        4 is represented by (0010011)
#        5 is represented by (1011011)
#        6 is represented by (1011111)
#        7 is represented by (1110000)
#        8 is represented by (1111111)
#        9 is represented by (1111011)
numbers = []
# 0 is even
numbers.append([1,1,1,1,1,1,0])
numbers.append([1])
# 1 is odd
numbers.append([0,1,1,0,0,0,0])
numbers.append([0])
# 2 is even
numbers.append([1,1,0,1,1,0,1])
numbers.append([1])
# 3 is odd
numbers.append([1,1,1,1,0,0,1])
numbers.append([0])
# 4 is even
numbers.append([0,0,1,0,0,1,1])
numbers.append([1])
# 5 is odd
numbers.append([1,0,1,1,0,1,1])
numbers.append([0])
# 6 is even
numbers.append([1,0,1,1,1,1,1])
numbers.append([1])
# 7 is odd
numbers.append([1,1,1,0,0,0,0])
numbers.append([0])
# 8 is even
numbers.append([1,1,1,1,1,1,1])
numbers.append([1])
# 9 is odd
numbers.append([1,1,1,1,0,1,1])
numbers.append([0])

execfile('weights.py')

# Create a new network
net = core.Network ()

# Create the input map
number = core.Map ( (1,7), (0,0) )
number.append(core.Layer())
number[0].fill(core.Unit)
number.name = 'number'
net.append(number)

# Create the focus map 
evenodd = core.Map ( (1,2), (1,0) )
evenodd.append (core.Layer())
evenodd[0].fill(learn.Unit)
evenodd.name = 'evenodd'

evenodd.spec = cnft.Spec()
evenodd.spec.tau      = 0.75
evenodd.spec.baseline = 0.0
evenodd.spec.alpha    = 1.0
evenodd.spec.min_act  = 0.0
evenodd.spec.max_act  = 1.0

net.append(evenodd)

proj          = projection.projection()
proj.self     = True
proj.distance = distance.euclidean(False)
proj.density  = density.full(1)
proj.shape    = shape.box(1,1)
proj.profile  = profile.uniform(0,0)
proj.src      = number[0]
proj.dst      = evenodd[0]
proj.connect()





learner = learn.Learner()

# Hebb's rule

learner.set_source(number[0])
learner.set_destination(evenodd[0])
learner.add_one([1,1,[1.0]])
learner.connect()

# Oja's rule
#learner.set_source(number[0])
#learner.set_destination(evenodd[0])
#learner.add_one([1,1,[1]])
#learner.add_one([2,0,[0,-1]])
#learner.connect()

#learner.learn(0.1); # The parameter is the learning rate

## Show network
netview = view.network.NetworkView (net)
weightsview = WeightsView(evenodd[0], number[0])

#manager = pylab.get_current_fig_manager()


def learn(nb_steps,lrate):
	for n in range(nb_steps):
		i=0
		for i in range((len(numbers))/2):
			# Set the input
			clamp_ex(i)
			# Make some steps
			net.evaluate(4,False)
			# Update the output value to take into account the desired output
			clamp_res(i)
			# Learn
			learner.learn(lrate)

def clamp_ex(i):
	num = numbers[2*i]
	for j in range(len(num)):
		number[0].unit(j).potential = num[j]

def clamp_res(i):
	res = numbers[2*i+1]
	evenodd.unit(0).potential = res[0] - evenodd.unit(0).potential
	evenodd.unit(1).potential = (1-res[0]) - evenodd.unit(1).potential

def test(i):
	# Clamp the representation of number i, make some steps, and get the result "odd or even"
	clamp_ex(i)
	net.evaluate(4,False)
	if (evenodd.unit(0).potential > 0.5):
		print "Number ",i,"is even"
	else:
		print "Number ",i,"is odd"

def init():
	for i in range(width*height):
		number[0].unit(i).potential = random.random()
		#evenodd[0].unit(i).potential = random.random()

def updatefig(*args):
    netview.update()
    weightsview.update()
    return True

gobject.idle_add (updatefig)
pylab.show()

