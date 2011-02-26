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
''' Management of time '''

second = 1
millisecond = 0.001
ms = millisecond


class Timer(object):
    ''' Description of a timer function '''

    _func = None
    _dt = 0
    _next = 0
    _order = 0
    _clock = None

    def __init__(self, func, clock, dt, order=0):
        ''' Create a new timer function to be called every dt.
        
        **Parameter**

        func : function(time)
            Function to be called every dt

        clock : Clock
            Clock that will trigger the timer

        dt : float
            Time interval between two calls

        order : int
            In case several timers share the same time interval, those with
            lower order are called first.
        '''
        self._func = func
        self._dt = dt
        self._next = 0
        self._order = order
        self._clock = clock

    def __call__(self):
        ''' Call the timer function and update local time '''
        self._func(self._next)
        self._next += self._dt

    def __cmp__(self, other):
        ''' Comparison function used to order timers '''
        return ( cmp(self._next, other._next)
                 or cmp(self._order,other._order) )





class Tick(object):
    ''' Clock decorator

    **Usage**

    clock = Clock()
    @clock.tick
    def timer(t): print 'called at time', t
    '''
    _func = None
    _clock = None

    def __init__(self, function):
        ''' Add function to the clock using default clock dt '''
        self._func = function
        self._clock.add(function)





class before(object):
    ''' Tick class decorator

    This is used to specify that a function is to be called just before the
    clock default tick. It must be used in conjunction with the Tick decorator.

    **Usage**

    clock = Clock()
    @before(clock.tick)
    def timer(t): print 'called at time', t
    '''

    def __init__(self, tick):
        ''' Register relevant clock tick.

        **Parameters**
        
        tick : Tick
            A tick decorator 
        '''
        self._tick = tick

    def __call__(self, func):
        ''' Add function to the clock using default clock dt '''
        self._tick._clock.add(func, order=-1)





class after(object):
    ''' Tick class decorator 

    This is used to specify that a function is to be called just after the
    clock default tick.

    **Usage**

    clock = Clock()
    @after(clock.tick)
    def timer(t): print 'called at time', t
    '''

    def __init__(self, tick):
        ''' Register relevant clock tick
        **Parameters**
        
        tick : Tick
            A tick decorator 
        '''
        self._tick = tick

    def __call__(self, func):
        ''' Add function to the clock using default clock dt '''
        self._tick._clock.add(func, order=+1)





class Every(object):
    ''' Clock decorator 

    This is used to specify that a function is to be called on a regular basis.

    **Usage**

    clock = Clock()
    @clock.every(0.1)
    def timer(t): print 'called at time', t
    '''

    _order = 0
    _dt = None
    _clock = None

    def __init__(self, dt, order=0):
        '''
        dt : float
            Time interval between two calls

        order : int
            In case several timers share the same time interval, those with
            lower order are called first.

        '''
        self._dt = dt
        self._order = order

    def __call__(self, func):
        ''' Add function to the clock using given dt and order. '''
        clock.add(func, self._dt, self._order)



class ClockException(Exception):
    ''' Clock Exception '''
    pass



class Clock(object):
    ''' Clock class '''

    _start   = 0.0*second
    _time    = 0.0*second
    _end     = 1.0*second
    _dt      = 1.0*millisecond
    _running = False
    _timers  = []
    
    def __init__(self, start=0.0, end=1.0, dt=0.001):
        ''' Initialize clock

        **Parameters**

        start : float
            Start time
        
        end : float
            End time

        dt : float
            Time step resolution
        '''
        self._start = start
        self._end = end
        self._dt = dt
        self._time = self._start
        self.every = Every
        self.every._clock = self
        self.tick = Tick
        self.tick._clock = self



    def reset(self):
        ''' Reset clock '''

        self._time = self._start
        for timer in self._timers:
            timer._next = self._start
        self._timers.sort()



    def clear(self):
        ''' Remove all timers '''

        self._timers = []



    def run(self, start=None, end=None, dt=None):
        ''' Run the clock.
        
        **Parameters**

        start : float
            Start time
        
        end : float
            End time

        dt : float
            Time step resolution
        '''
        self.start = start or self._start
        self.end = end or self._end
        self._dt = dt or self._dt

        self._running = True
        while self._time <= self._end and self._running:
            # print 'Tick : %.3f' % self.time
            while self._timers[0]._next < (self._time+self._dt) and self._running:
                timer = self._timers[0]
                if timer._next <= self._end and \
                        self._time + self._dt - timer._next > 1e-10:
                    timer()
                else:
                    #self._running = False
                    break
                self._timers.sort()
            self._time += self._dt


                
    def stop(self):
        ''' Stop the clock. '''

        self._running = False
        


    def add(self, func, dt=None, order=0):
        ''' Add a new timer to the timer list

        **Parameters**

        func : function(time)
            Function to be added

        dt : float or None
            Time interval between each function call. If not timestep is given,
            clock resolution (clock.dt) is used.

        order : int
            In case several timers share the same time interval, those with
            lower order are called first.
        '''

        if not dt:
            dt = self._dt
        timer = Timer(func, self, dt, order)
        self._timers.append(timer)
        self._timers.sort()



    def remove(self, func, dt=None):
        ''' Remove a given timer from the timer list

        **Parameters**

        func : function(time)
            Function to be removed

        dt : float or None
            Function timestep (as it was given when this function has been
            added to the timer list). If not timestep is given, clock
            resolution (clock.dt) is used.

        **Notes**

        A same function can be added with several different timesteps. It is
        this necessary to specify which timer (using timestep) is to be
        removed.
        '''

        if not dt:
            dt = self._dt
        for i in range(len(self._timers)):
            timer = self._timers[i]
            if timer._func == func and timer._dt == dt:
                self._timers.pop(i)
                break

    def _get_time(self):
        ''' Return current time '''
        return self._time
    time = property(_get_time,
                    doc = '''Current time''')

    def _get_start(self):
        ''' Return start time '''
        return self._start
    def _set_start(self, time):
        ''' Set start time '''
        if self._running:
            raise ClockException('Cannot set start time while running')
        if self._end < self._start:
            raise ClockException('Start time must be inferor to end time')
        self._start = time
        self.reset()
    start = property(_get_start, _set_start,
                     doc = '''Clock start time''')

    def _get_end(self):
        ''' Return end time '''
        return self._end
    def _set_end(self, time):
        ''' Set end time '''
        if self._running:
            raise ClockException('Cannot set end time while running.')
        if self._end < self._start:
            raise ClockException('End time must be superior to start time.')
        self._end = time
        self.reset()
    end = property(_get_end, _set_end,
                     doc = '''Clock end time.''')



    def _get_dt(self):
        ''' Return clock resolution. '''
        return self._dt
    def _set_dt(self, dt):
        ''' Set clock resolution. '''
        if self._running:
            raise ClockException('Cannot set resolution while running.')
        previous_dt = self._dt
        self._dt = dt
        self.reset()
        for timer in self._timers:
            if timer._dt == previous_dt:
                timer._dt = dt
    dt = property(_get_dt, _set_dt,
                  doc = '''Clock resolution.''')





# -----------------------------------------------------------------------------
if __name__ == '__main__':

    clock = Clock(end=1.0, dt=0.1)
    @clock.tick

    def timer_2(time):
        print 'timer 2 called at time %.3f' % time

    @before(clock.tick)
    def timer_1(time):
        print 'timer 1 called at time %.3f' % time

    @after(clock.tick)
    def timer_3(time):
        print 'timer 3 called at time %.3f' % time

    @clock.every(100*millisecond,-1)
    def timer_4(time): print 'timer 4 called at time %.3f' % time

    @clock.every(100*millisecond,+1)
    def timer_5(time): print 'timer 5 called at time %.3f' % time

    clock.run()
