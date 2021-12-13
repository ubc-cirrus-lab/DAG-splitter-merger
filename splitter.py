from mip import *

class Splitter:
    difficultyDecentFactor = 0.8

    def SuggestSplit(self, splitCandidates, minDesiredServerPoolReduction,
        leftCPUPoolCapacity, leftMemoryPoolCapacity, verbose):
        """
        Returns a list of 0's (no splitting recommendations) and 1's (splitting recommendations)
        """
        r = 1

        while (True):
            model = Model(sense=MINIMIZE, solver_name=CBC)

            x = [model.add_var(var_type=BINARY) for s in splitCandidates]
            model.objective = xsum( [x[i]*splitCandidates[i].GetSplitCommBW() \
                                    for i in range(len(x))] )

            # constraints to limit the max splitting, to maintain merged elements for performance
            model.add_constr( xsum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='C') \
                                for i in range(len(x))] ) >= r*minDesiredServerPoolReduction['cores'],
                                priority=1)
            model.add_constr( xsum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='M') \
                                for i in range(len(x))] ) >= r*minDesiredServerPoolReduction['mem'],
                                priority=1)
            # constraints to respect resources available on the CPU Pool
            model.add_constr( xsum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='C', objectType='c') \
                                for i in range(len(x))] ) <= leftCPUPoolCapacity['cores'],
                                priority=2)
            model.add_constr( xsum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='M', objectType='c') \
                                for i in range(len(x))] ) <= leftCPUPoolCapacity['mem'],
                                priority=2)
            # constraints to respect resources available on the Memory Pool
            model.add_constr( xsum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='C', objectType='m') \
                                for i in range(len(x))] ) <= leftMemoryPoolCapacity['cores'],
                                priority=2)
            model.add_constr( xsum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='M', objectType='m') \
                                for i in range(len(x))] ) <= leftMemoryPoolCapacity['mem'],
                                priority=2)

            status = model.optimize(max_seconds=30)
            if verbose:
                print(status)

            # check if no solution was found, each the condition
            if [x[i].x for i in range(len(x))] == [None for i in range(len(x))]:
                print("No solution could be found! Easing the minDesiredServerPoolReduction constraint.")
                r *= self.difficultyDecentFactor
            else:
                break

        splittingDecisions = [x[i].x for i in range(len(x))]
        return splittingDecisions