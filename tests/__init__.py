#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

def test_suite():
    suite = unittest.TestLoader().discover(start_dir=".")
    return suite