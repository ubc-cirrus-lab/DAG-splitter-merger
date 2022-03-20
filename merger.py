from mip import *


class Merger:
    def SuggestMerge(
        self, mergeCandidates, maxServerPoolAllowanceForMerging, serverSize
    ):
        """
        Returns a list of 0's (no merging recommendations) and 1's (merging recommendations)
        """
        model = Model(sense=MAXIMIZE, solver_name=CBC)

        x = [model.add_var(var_type=BINARY) for s in mergeCandidates]
        model.objective = xsum(
            [x[i] * mergeCandidates[i].GetSplitCommBW() for i in range(len(x))]
        )

        # constraints to respect Server Pool resources (maxServerPoolAllowanceForMerging)
        model.add_constr(
            xsum(
                [
                    x[i] * mergeCandidates[i].GetTotalResources(resourceType="C")
                    for i in range(len(x))
                ]
            )
            <= maxServerPoolAllowanceForMerging["cores"],
            priority=1,
        )
        model.add_constr(
            xsum(
                [
                    x[i] * mergeCandidates[i].GetTotalResources(resourceType="M")
                    for i in range(len(x))
                ]
            )
            <= maxServerPoolAllowanceForMerging["mem"],
            priority=1,
        )
        # constraints to respect each server size
        for i in range(len(mergeCandidates)):
            model.add_constr(
                x[i] * mergeCandidates[i].GetTotalResources(resourceType="C")
                <= serverSize["cores"],
                priority=1,
            )
            model.add_constr(
                x[i] * mergeCandidates[i].GetTotalResources(resourceType="M")
                <= serverSize["mem"],
                priority=1,
            )

        model.optimize(max_seconds=30)

        mergingDecisions = [x[i].x for i in range(len(x))]
        return mergingDecisions
