class Element:
    types = None
    coreUsageMetric = None
    memUsageMetric = None
    communicationMetric = None

    def __init__(self, types, coreUsageMetric, memUsageMetric, communicationMetric):
        if (
            self.CheckMetricValidity(
                types, coreUsageMetric, memUsageMetric, communicationMetric
            )
            == False
        ):
            raise ValueError("Ivalid element metrics!")
        self.types = types.copy()
        self.coreUsageMetric = coreUsageMetric.copy()
        self.memUsageMetric = memUsageMetric.copy()
        self.communicationMetric = communicationMetric.copy()

    def CheckMetricValidity(
        self, types, coreUsageMetric, memUsageMetric, communicationMetric
    ):
        if (
            (len(types) != len(coreUsageMetric))
            or (len(types) != len(memUsageMetric))
            or (len(types) != len(communicationMetric))
        ):
            return False
        if len(types) != 0:
            lenComps = [len(x) - len(types) for x in communicationMetric]
            for lenComp in lenComps:
                if lenComp != 0:
                    return False
        for t in types:
            if (t != "c") and (t != "m"):
                return False
        return True

    def GetTotalResources(self, resourceType, objectType=None):
        if objectType is None:
            if resourceType == "C":
                return sum(self.coreUsageMetric)
            elif resourceType == "M":
                return sum(self.memUsageMetric)
        else:
            if resourceType == "C":
                return sum(
                    [
                        self.coreUsageMetric[i]
                        for i in range(len(self.types))
                        if self.types[i] == objectType
                    ]
                )
            elif resourceType == "M":
                return sum(
                    [
                        self.memUsageMetric[i]
                        for i in range(len(self.types))
                        if self.types[i] == objectType
                    ]
                )

    def GetSplitCommBW(self):
        splitCommBW = sum([sum(x) for x in self.communicationMetric])
        # remove communication bandwidth of each object to itself
        splitCommBW -= sum(
            [
                self.communicationMetric[i][i]
                for i in range(len(self.communicationMetric))
            ]
        )
        # divide by 2 to eliminate duplicate counting
        splitCommBW /= 2
        return splitCommBW
