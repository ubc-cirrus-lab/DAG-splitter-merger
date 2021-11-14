from mip import Model, MAXIMIZE, CBC, BINARY, INTEGER, OptimizationStatus

class Splitter:
    def SuggestSplit(self, splitCandidates, desiredServerPoolReduction,
                leftCPUPoolCapacity, leftMemoryPoolCapacity):
        
        model = Model(sense=MAXIMIZE, solver_name=CBC)

        # for i in range(len(splitCandidates)):
        #     splitCandidate = splitCandidates[i]
        
        x = [model.add_var(var_type=BINARY) for s in splitCandidates]
        model.objective = sum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='C') \
                                + x[i]*splitCandidates[i].GetTotalResources(resourceType='M') \
                                for i in range(len(x))] )

        model.add_constr( sum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='C', objectType='c') \
                                for i in range(len(x))] ) <= leftCPUPoolCapacity['cores'])
        model.add_constr( sum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='M', objectType='c') \
                                for i in range(len(x))] ) <= leftCPUPoolCapacity['mem'])
        model.add_constr( sum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='C', objectType='m') \
                                for i in range(len(x))] ) <= leftMemoryPoolCapacity['cores'])
        model.add_constr( sum( [x[i]*splitCandidates[i].GetTotalResources(resourceType='M', objectType='m') \
                                for i in range(len(x))] ) <= leftMemoryPoolCapacity['mem'])
        
        status = model.optimize(max_seconds=20)
        print(status)
        return [x[i].x for i in range(len(x))]
