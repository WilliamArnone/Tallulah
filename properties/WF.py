from copy import deepcopy, error
from errno import EROFS
import itertools
from Graph import EdgeToString, Graph

#No infinite reverse computation
#we do not have Pi:= Pi+1-αi->Pi for all i = 0,1,...

class WF:

    name = "WF - Well-Foundedness"

    def Check(graph:Graph):#, getMinEdges=True):
        """Check WF property and return true if holds"""
        #a dot file is finite, the only way to make an infinite length paths is to make a cycle
    
        errors = set()
        not_visited = deepcopy(graph.nodes)
        path = []

        #keep search until all node are visited
        while len(not_visited)>0:
            node = list(not_visited)[0]
            
            #call recursive bfs algorithm
            sub_errors = WF.__BFS(graph, node, path, not_visited)

            #append to errors the cycle nodes
            for index in range(len(sub_errors)): 
                next = index+1 if index < len(sub_errors)-1 else -1
                for error in graph.GetEdgesBetween(sub_errors[index], sub_errors[next], all=False): 
                    errors.add(error)
                    
        return list(errors)

    def __BFS(graph:Graph, node, path, not_visited):
        """BFS algorithm in order to find cycles"""
        errors = []
        #if there is a cycle
        if node in path:
            start_cycle=False
            errors.append(node)
            #we return only the nodes of the cycle
            for index in range(len(path)):
                if path[index]==node: start_cycle=True
                if start_cycle: errors.append(path[index])
            errors.append(node)
            return errors
        
        path.append(node)

        #foreach adjacent node we apply the recursion
        for adj_node in graph.GetAdj(node):
            if(adj_node in not_visited):
                sub_errors = WF.__BFS(graph, adj_node, path, not_visited)
                errors.extend(sub_errors)

        #this node is fully visited
        not_visited.remove(node)
        path.pop()

        return errors

    def Apply(graph: Graph, error):
        """Remove WF errors from the graph"""
        graph.RemoveEdge(error)
    
    def IsApplyable(error):
        """Returns True if the error can be fixed"""
        return True

    def GetLog(error):
        """Returns the BTI errors in a (text, color) list"""
        log = []
        log.append((EdgeToString(error), "red"))
        log.append(('creates a cycle', "black"))
        return log