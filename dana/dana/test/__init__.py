#!/usr/bin/env python
#
# Copyright (c) 2006-2007 Nicolas Rougier.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
# 
# $Id$
""" Regression tests """

import sys
import unittest
import unit,layer,map

def test(verbosity=2):
    """ Perform dana regression tests """
    
    suite = unittest.TestSuite()
    suite.addTest (unit.suite)
    suite.addTest (layer.suite)
    suite.addTest (map.suite)
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=verbosity)
    result = runner.run(suite)
    return result
