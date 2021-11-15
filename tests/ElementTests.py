import sys
import unittest
sys.path.insert(0, '.')
sys.path.insert(0, '..')
from element import Element

class TestElement(unittest.TestCase):
    e1 = Element(types=['c', 'm'],
            coreUsageMetric=[1, 0.2],
            memUsageMetric= [52, 245],
            communicationMetric=[[0, 120], [120,0]])
    e2 = Element(types=['c', 'm', 'c'],
            coreUsageMetric=[1, 0.2, 2],
            memUsageMetric= [52, 245, 48],
            communicationMetric=[[1000, 120, 540], [120, 1000, 800], [540, 800, 63]])

    def test_GetTotalResources(self):
        core = self.e1.GetTotalResources(resourceType='C')
        mem = self.e1.GetTotalResources(resourceType='M')
        self.assertEqual([core, mem], [1.2, 297])

    def test_GetTotalResourcesPerObject(self):
        coreC = self.e1.GetTotalResources(resourceType='C', objectType='c')
        memC = self.e1.GetTotalResources(resourceType='M', objectType='c')
        coreM = self.e1.GetTotalResources(resourceType='C', objectType='m')
        memM = self.e1.GetTotalResources(resourceType='M', objectType='m')
        self.assertEqual([coreC, memC, coreM, memM], [1, 52, 0.2, 245])

    def test_GetSplitCommBW(self):
        e1Res = self.e1.GetSplitCommBW()
        e2Res = self.e2.GetSplitCommBW()
        self.assertEqual([e1Res, e2Res], [120, 1460])

if __name__ == '__main__':
    unittest.main()