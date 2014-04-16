#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: unittest.recipe.py
Creation: 2014-1-3
Revision: 2014-1-3
"""

#===============================================================================
# 测试random的三个功能
#     1. random.shuffle
#     2. random.choice
#     3. random.sample
#==============================================================================

import random
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1, 2, 3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)


# if __name__ == '__main__':
#     unittest.main()

#===============================================================================
# alternative way to run this code in shell script
#===============================================================================

suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)