import logging
import numpy as np
import random
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")
from candidate import Candidate
from merger import Merger
from splitter import Splitter


def CreateRandomCandidate(
    maxSize, maxCorePerSubCandidate, maxMemMBPerSubCandidate, maxCommunication
):
    size = random.randint(2, maxSize)
    types = ["c" if x == 0 else "m" for x in list(np.random.randint(0, 2, size))]
    coreUsageMetric = [
        x / 1000 for x in list(np.random.randint(0, maxCorePerSubCandidate * 1000, size))
    ]
    memUsageMetric = [
        x / 1000 for x in list(np.random.randint(0, maxMemMBPerSubCandidate * 1000, size))
    ]
    communicationMetric = [[0 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(i, size):
            communicationMetric[i][j] = (
                random.randint(0, maxCommunication * 1000) / 1000
            )
            communicationMetric[j][i] = communicationMetric[i][j]
    log = (
        str(types)
        + str(coreUsageMetric)
        + str(memUsageMetric)
        + str(communicationMetric)
    )
    return [
        Candidate(
            types=types,
            coreUsageMetric=coreUsageMetric,
            memUsageMetric=memUsageMetric,
            communicationMetric=communicationMetric
        ),
        log,
    ]


def RunFuzzer(scenarioCount, minCandidates, maxCandidates, mode):
    merger = Merger()
    splitter = Splitter()

    for scenario in range(scenarioCount):
        # logging.debug('Scenario '+str(scenario+1)+'/'+str(scenarioCount))
        candidateCount = random.randint(minCandidates, maxCandidates)
        logCombined = ""
        candidates = []
        for i in range(candidateCount):
            candidate, log = CreateRandomCandidate(
                maxSize=20,
                maxCorePerSubCandidate=10,
                maxMemMBPerSubCandidate=1024,
                maxCommunication=1024
            )
            candidates.append(candidate)
            logCombined += log + " "

        try:
            if mode == "merge":
                maxServerPoolAllowanceForMerging = {
                    "cores": random.randint(0, 400),
                    "mem": random.randint(0, 102400)
                }
                serverSize = {
                    "cores": random.randint(10, 40),
                    "mem": random.randint(5120, 10240)
                }
                decisions = merger.SuggestMerge(
                    mergeCandidates=candidates,
                    maxServerPoolAllowanceForMerging=maxServerPoolAllowanceForMerging,
                    serverSize=serverSize,
                )
            elif mode == "split":
                minDesiredServerPoolReduction = {
                    "cores": random.randint(0, 400),
                    "mem": random.randint(0, 102400)
                }
                leftCPUPoolCapacity = {
                    "cores": random.randint(0, 400),
                    "mem": random.randint(0, 102400)
                }
                leftMemoryPoolCapacity = {
                    "cores": random.randint(0, 400),
                    "mem": random.randint(0, 102400)
                }
                decisions = splitter.SuggestSplit(
                    splitCandidates=candidates,
                    minDesiredServerPoolReduction=minDesiredServerPoolReduction,
                    leftCPUPoolCapacity=leftCPUPoolCapacity,
                    leftMemoryPoolCapacity=leftMemoryPoolCapacity
                )
        except:
            logging.debug(
                "Offending scenario: " + str(scenario + 1) + "/" + str(scenarioCount)
            )
            logging.debug("Candidate count: " + str(candidateCount))
            logging.debug("Candidate details: " + logCombined)
            if mode == "merge":
                logging.debug(
                    "maxServerPoolAllowanceForMerging,serverSize: "
                    + str([maxServerPoolAllowanceForMerging, serverSize])
                )
            elif mode == "split":
                logging.debug(
                    "minDesiredServerPoolReduction,leftCPUPoolCapacity,leftMemoryPoolCapacity: "
                    + str(
                        [
                            minDesiredServerPoolReduction,
                            leftCPUPoolCapacity,
                            leftMemoryPoolCapacity
                        ]
                    )
                )
            logging.debug(decisions)
            pass


if __name__ == "__main__":
    logging.basicConfig(
        filename="fuzzer.log",
        level=logging.DEBUG,
        format="%(asctime)s %(message)s",
        filemode="w"
    )
    # RunFuzzer(scenarioCount=1000000, minCandidates=1, maxCandidates=50, mode="merge")
    RunFuzzer(scenarioCount=100, minCandidates=1, maxCandidates=50, mode="split")
