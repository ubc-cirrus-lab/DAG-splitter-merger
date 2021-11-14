import sys
import unittest
sys.path.insert(0, '.')
sys.path.insert(0, '..')
from element import Element
from splitter import Splitter

class TestSplitting(unittest.TestCase):
    splitter = Splitter()

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
                                                        desiredServerPoolReduction={'cores': 20, 'mem':1024}, 
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':20}, 
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':40960})
        self.assertEqual(splittingDecisions, [0, 0, 0]) # no splitting should be recommended
    
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
                                                        desiredServerPoolReduction={'cores': 20, 'mem':1024}, 
                                                        leftCPUPoolCapacity={'cores': 0.1, 'mem':10240}, 
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':40960})
        self.assertEqual(splittingDecisions, [0, 0, 0]) # no splitting should be recommended

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
                                                        desiredServerPoolReduction={'cores': 20, 'mem':1024}, 
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':10240}, 
                                                        leftMemoryPoolCapacity={'cores': 50, 'mem':20})
        self.assertEqual(splittingDecisions, [0, 0, 0]) # no splitting should be recommended
    
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
                                                        desiredServerPoolReduction={'cores': 20, 'mem':1024}, 
                                                        leftCPUPoolCapacity={'cores': 100, 'mem':10240}, 
                                                        leftMemoryPoolCapacity={'cores': 0.1, 'mem':40960})
        self.assertEqual(splittingDecisions, [0, 0, 0]) # no splitting should be recommended

if __name__ == '__main__':
    unittest.main()