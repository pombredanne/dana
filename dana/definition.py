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
'''
Generic definition of type:

* :class:`DifferentialEquation` (``dY/dt = expr : type``)
* :class:`Equation` (``Y = expr : type``)
* :class:`Declaration` (``Y : type``)
'''

class DefinitionError(Exception):
    ''' Definition Error '''
    pass


class Definition(object):
    ''' Generic definition of type:

    * :class:`DifferentialEquation` (``dY/dt = expr : type``)
    * :class:`Equation` (``Y = expr : type``)
    * :class:`Declaration` (``Y : type``)
    '''
  
    def __init__(self, definition):
        self._definition = None
        self._varname = None
        self._dtype = None

    def _parse(self, definition):
        ''' Parse definition '''
        raise NotImplemented(definition)

    def __repr__(self):
        ''' x.__repr__() <==> repr(x) '''

        classname = self.__class__.__name__
        return "%s('%s = %s : %s')" % (classname, self._lhs, self._rhs, self._dtype)


    def _get_varname(self):
        ''' Get variable name (left hand side) '''
        return self._varname
    varname = property(_get_varname,
                       doc='''Equation variable name (left hand side) ''')

    def _get_lhs(self):
        ''' Get equation left hand side '''
        return self._lhs
    lhs = property(_get_lhs,
                   doc='''Equation left hand-side''')

    def _get_rhs(self):
        ''' Get equation right hand side '''
        return self._rhs
    rhs = property(_get_lhs,
                   doc='''Equation right hand-side''')

    def _get_definition(self):
        ''' Get equation original definition '''
        return self._definition
    definition = property(_get_definition,
                          doc='''Equation original definition''')

    def _get_dtype(self):
        '''Get equation data type '''
        return self._dtype
    dtype = property(_get_dtype,
                     doc='''Equation data type''')


