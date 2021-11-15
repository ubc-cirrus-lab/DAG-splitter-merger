import sys
import unittest
sys.path.insert(0, '.')
sys.path.insert(0, '..')
from element import Element
from splitter import Splitter

class TestSplitting(unittest.TestCase):
    splitter = Splitter()

    def test_NoSplittingNeeded(self):
        e1 = Element(types=['c','m'],
            coreUsageMetric=[1, 0.2], memUsageMetric= [52, 245],
            communicationMetric=[[0, 120], [120,0]])
        e2 = Element(types=['c','m'],
            coreUsageMetric=[0.8, 0.5], memUsageMetric= [158, 652],
            communicationMetric=[[0, 840], [840,0]])
        e3 = Element(types=['c','m'],
            coreUsageMetric=[1, 1], memUsageMetric= [26, 39],
            communicationMetric=[[0, 30], [30,0]])
        splittingDecisions = self.splitter.SuggestSplit(splitCandidates=[e1, e2, e3],
                                                        minDesiredServerPoolReduction={'cores': 0, 'mem':0},
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':10240},
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':40960},
                                                        verbose=False)
        # no demand expressed in minDesiredServerPoolReduction => no splitting needed
        self.assertEqual(splittingDecisions, [0, 0, 0])

    def test_OneSplittingNeeded(self):
        e1 = Element(types=['c','m'],
            coreUsageMetric=[1, 0.2], memUsageMetric= [52, 245],
            communicationMetric=[[0, 120], [120,0]])
        e2 = Element(types=['c','m'],
            coreUsageMetric=[0.8, 0.5], memUsageMetric= [158, 652],
            communicationMetric=[[0, 840], [840,0]])
        e3 = Element(types=['c','m'],
            coreUsageMetric=[1, 1], memUsageMetric= [26, 39],
            communicationMetric=[[0, 30], [30,0]])
        splittingDecisions = self.splitter.SuggestSplit(splitCandidates=[e1, e2, e3],
                                                        minDesiredServerPoolReduction={'cores': 1, 'mem':10},
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':10240},
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':40960},
                                                        verbose=False)
        # to free up 1 core and 0 memory, splitting e3 is enough and
        # would have the smallest object-to-obejct communication bandwidth
        self.assertEqual(splittingDecisions, [0, 0, 1])

    def test_TwoSplittingsNeeded(self):
        e1 = Element(types=['c','m'],
            coreUsageMetric=[1, 0.2], memUsageMetric= [52, 245],
            communicationMetric=[[0, 120], [120,0]])
        e2 = Element(types=['c','m'],
            coreUsageMetric=[0.8, 0.5], memUsageMetric= [158, 652],
            communicationMetric=[[0, 840], [840,0]])
        e3 = Element(types=['c','m'],
            coreUsageMetric=[1, 1], memUsageMetric= [26, 39],
            communicationMetric=[[0, 30], [30,0]])
        splittingDecisions = self.splitter.SuggestSplit(splitCandidates=[e1, e2, e3],
                                                        minDesiredServerPoolReduction={'cores': 1.2, 'mem':1024},
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':10240},
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':40960},
                                                        verbose=False)
        # splitting e1 and e2 would reduce 2.5 cores and 1107 MB of memory
        # meeting the demand from minDesiredServerPoolReduction
        self.assertEqual(splittingDecisions, [1, 1, 0])

    def test_AllSplittingsNeededDespiteNotEnough(self):
        e1 = Element(types=['c','m'],
            coreUsageMetric=[1, 0.2], memUsageMetric= [52, 245],
            communicationMetric=[[0, 120], [120,0]])
        e2 = Element(types=['c','m'],
            coreUsageMetric=[0.8, 0.5], memUsageMetric= [158, 652],
            communicationMetric=[[0, 840], [840,0]])
        e3 = Element(types=['c','m'],
            coreUsageMetric=[1, 1], memUsageMetric= [26, 39],
            communicationMetric=[[0, 30], [30,0]])
        splittingDecisions = self.splitter.SuggestSplit(splitCandidates=[e1, e2, e3],
                                                        minDesiredServerPoolReduction={'cores': 20, 'mem':50},
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':10240},
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':40960},
                                                        verbose=False)
        # all splitting should happen despite it falling short of
        # minDesiredServerPoolReduction demanded
        self.assertEqual(splittingDecisions, [1, 1, 1])

    def test_TooLittleMemoryLeftInCPUPool(self):
        e1 = Element(types=['c','m'],
            coreUsageMetric=[1, 0.2], memUsageMetric= [52, 245],
            communicationMetric=[[0, 120], [120,0]])
        e2 = Element(types=['c','m'],
            coreUsageMetric=[0.8, 0.5], memUsageMetric= [158, 652],
            communicationMetric=[[0, 840], [840,0]])
        e3 = Element(types=['c','m'],
            coreUsageMetric=[1, 1], memUsageMetric= [26, 39],
            communicationMetric=[[0, 30], [30,0]])
        splittingDecisions = self.splitter.SuggestSplit(splitCandidates=[e1, e2, e3],
                                                        minDesiredServerPoolReduction={'cores': 20, 'mem':1024},
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':20},
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':40960},
                                                        verbose=False)
        # no splitting should be recommended as the CPU pool
        # will run out of memory even with the smallest split
        self.assertEqual(splittingDecisions, [0, 0, 0])

    def test_TooFewCoresLeftInCPUPool(self):
        e1 = Element(types=['c','m'],
            coreUsageMetric=[1, 0.2], memUsageMetric= [52, 245],
            communicationMetric=[[0, 120], [120,0]])
        e2 = Element(types=['c','m'],
            coreUsageMetric=[0.8, 0.5], memUsageMetric= [158, 652],
            communicationMetric=[[0, 840], [840,0]])
        e3 = Element(types=['c','m'],
            coreUsageMetric=[1, 1], memUsageMetric= [26, 39],
            communicationMetric=[[0, 30], [30,0]])
        splittingDecisions = self.splitter.SuggestSplit(splitCandidates=[e1, e2, e3],
                                                        minDesiredServerPoolReduction={'cores': 20, 'mem':1024},
                                                        leftCPUPoolCapacity={'cores': 0.1, 'mem':10240},
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':40960},
                                                        verbose=False)
        # no splitting should be recommended as the CPU pool
        # will run out of cores even with the smallest split
        self.assertEqual(splittingDecisions, [0, 0, 0])

    def test_TooLittleMemoryLeftInMemoryPool(self):
        e1 = Element(types=['c','m'],
            coreUsageMetric=[1, 0.2], memUsageMetric= [52, 245],
            communicationMetric=[[0, 120], [120,0]])
        e2 = Element(types=['c','m'],
            coreUsageMetric=[0.8, 0.5], memUsageMetric= [158, 652],
            communicationMetric=[[0, 840], [840,0]])
        e3 = Element(types=['c','m'],
            coreUsageMetric=[1, 1], memUsageMetric= [26, 39],
            communicationMetric=[[0, 30], [30,0]])
        splittingDecisions = self.splitter.SuggestSplit(splitCandidates=[e1, e2, e3],
                                                        minDesiredServerPoolReduction={'cores': 20, 'mem':1024},
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':10240},
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':20},
                                                        verbose=False)
        # no splitting should be recommended as the Memory pool
        # will run out of memory even with the smallest split
        self.assertEqual(splittingDecisions, [0, 0, 0])

    def test_TooFewCoresLeftInMemoryPool(self):
        e1 = Element(types=['c','m'],
            coreUsageMetric=[1, 0.2], memUsageMetric= [52, 245],
            communicationMetric=[[0, 120], [120,0]])
        e2 = Element(types=['c','m'],
            coreUsageMetric=[0.8, 0.5], memUsageMetric= [158, 652],
            communicationMetric=[[0, 840], [840,0]])
        e3 = Element(types=['c','m'],
            coreUsageMetric=[1, 1], memUsageMetric= [26, 39],
            communicationMetric=[[0, 30], [30,0]])
        splittingDecisions = self.splitter.SuggestSplit(splitCandidates=[e1, e2, e3],
                                                        minDesiredServerPoolReduction={'cores': 20, 'mem':1024},
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':10240},
                                                        leftMemoryPoolCapacity={'cores': 0.1, 'mem':40960},
                                                        verbose=False)
        # no splitting should be recommended as the Memory pool
        # will run out of cores even with the smallest split
        self.assertEqual(splittingDecisions, [0, 0, 0])

if __name__ == '__main__':
    unittest.main()