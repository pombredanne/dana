#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright INRIA
# Contributors: Nicolas P. Rougier (Nicolas.Rougier@inria.fr)
#
# DANA is a computing framework for the simulation of distributed,
# asynchronous, numerical and adaptive models.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL
# http://www.cecill.info/index.en.html.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# -----------------------------------------------------------------------------
from dana.time import Clock

clock = Clock(0.0, 1.0, 0.001)


class NetworkError(Exception):
    ''' '''
    pass





class Network(object):
    ''' '''

    def __init__(self, groups=[]):
        ''' '''
        self._groups = groups



    def setup(self):
        ''' '''
        for group in self._groups:
            group.setup()



    def run(self, time=1.0, dt=0.01, n=None):
        ''' '''

        if n != None:
            clock.end = n
            clock.dt = 1.0
        else:
            clock.end = time
            clock.dt = dt
        setup()
        clock.remove(self.evaluate)
        clock.add(self.evaluate)
        clock.run()


    def evaluate(self,time):
        ''' '''
        for group in self._groups:
            group.evaluate(dt=clock.dt)

        

    def append(self, group):
        ''' '''
        if group not in self._groups:
            self._groups.append(group)
        else:
            raise NetworkError, 'Group is already in network'



__default_network__ = Network([])


def run(time=1.0, dt=0.001, n=None):
    ''' '''
    __default_network__.run(time, dt, n)


def setup():
    ''' '''
    __default_network__.setup()
