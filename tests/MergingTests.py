import sys
import unittest

sys.path.insert(0, ".")
sys.path.insert(0, "..")
from candidate import Candidate
from merger import Merger


class TestMerging(unittest.TestCase):
    merger = Merger()

    def test_NoCandidateProvided(self):
        mergingDecisions = self.merger.SuggestMerge(
            mergeCandidates=[],
            maxServerPoolAllowanceForMerging={"cores": 80, "mem": 20480},
            serverSize={"cores": 40, "mem": 10240}
        )
        # the SuggestMerge function should still work even if no candidates are provided
        self.assertEqual(mergingDecisions, [])

    def test_NoMergingPossible1(self):
        e1 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[1, 0.2],
            memUsageMetric=[52, 245],
            communicationMetric=[[0, 120], [120, 0]]
        )
        e2 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[0.8, 0.5],
            memUsageMetric=[158, 652],
            communicationMetric=[[0, 840], [840, 0]]
        )
        e3 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[1, 1],
            memUsageMetric=[26, 39],
            communicationMetric=[[0, 30], [30, 0]]
        )
        mergingDecisions = self.merger.SuggestMerge(
            mergeCandidates=[e1, e2, e3],
            maxServerPoolAllowanceForMerging={"cores": 0, "mem": 0},
            serverSize={"cores": 40, "mem": 10240}
        )
        # given no resource allowance for the Server Pool nothing should be merged
        self.assertEqual(mergingDecisions, [0, 0, 0])

    def test_NoMergingPossible2(self):
        e1 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[1, 0.2],
            memUsageMetric=[52, 245],
            communicationMetric=[[0, 120], [120, 0]]
        )
        e2 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[0.8, 0.5],
            memUsageMetric=[158, 652],
            communicationMetric=[[0, 840], [840, 0]]
        )
        e3 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[1, 1],
            memUsageMetric=[26, 39],
            communicationMetric=[[0, 30], [30, 0]]
        )
        mergingDecisions = self.merger.SuggestMerge(
            mergeCandidates=[e1, e2, e3],
            maxServerPoolAllowanceForMerging={"cores": 1.1, "mem": 64},
            serverSize={"cores": 40, "mem": 10240}
        )
        # as the minimum resources for each candidate go beyond limits
        # of maxServerPoolAllowanceForMerging, nothing should be merged
        self.assertEqual(mergingDecisions, [0, 0, 0])

    def test_AllShouldBeMerged(self):
        e1 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[1, 0.2],
            memUsageMetric=[52, 245],
            communicationMetric=[[0, 120], [120, 0]]
        )
        e2 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[0.8, 0.5],
            memUsageMetric=[158, 652],
            communicationMetric=[[0, 840], [840, 0]]
        )
        e3 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[1, 1],
            memUsageMetric=[26, 39],
            communicationMetric=[[0, 30], [30, 0]]
        )
        mergingDecisions = self.merger.SuggestMerge(
            mergeCandidates=[e1, e2, e3],
            maxServerPoolAllowanceForMerging={"cores": 80, "mem": 20480},
            serverSize={"cores": 40, "mem": 10240}
        )
        # given the resource limits, everything can be merged
        self.assertEqual(mergingDecisions, [1, 1, 1])

    def test_ServerSizeLimits(self):
        e1 = Candidate(
            types=["c", "m"],
            coreUsageMetric=[1, 0.2],
            memUsageMetric=[52, 245],
            communicationMetric=[[0, 120], [120, 0]]
        )
        e2 = Candidate(
            types=["c", "c", "m"],
            coreUsageMetric=[20, 20, 1],
            memUsageMetric=[200, 200, 480],
            communicationMetric=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        )
        mergingDecisions = self.merger.SuggestMerge(
            mergeCandidates=[e1, e2],
            maxServerPoolAllowanceForMerging={"cores": 80, "mem": 20480},
            serverSize={"cores": 40, "mem": 10240}
        )
        # while e1 can be merged, merging objects of e2
        # would exceed the provided server size's cores (21>20)
        # thus e2 should not be merged
        self.assertEqual(mergingDecisions, [1, 0])


if __name__ == "__main__":
    unittest.main()
