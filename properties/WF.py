from copy import deepcopy, error
from errno import EROFS
import itertools
from Graph import EdgeToString, Graph

#No infinite reverse computation
#we do not have Pi:= Pi+1-αi->Pi for all i = 0,1,...

class WF:

    def Check(self, graph:Graph, getMinEdges=True):
        """Check WF property and return true if holds"""
        #a dot file is finite, the only way to make an infinite length paths is to make a cycle
        
        errors = set()
        not_visited = deepcopy(graph.nodes)
        path = []

        #keep search until all node are visited
        while len(not_visited)>0:
            node = list(not_visited)[0]
            
            #call recursive bfs algorithm
            sub_errors = self.__BFS(graph, node, path, not_visited)

            #append to errors the cycle nodes
            for index in range(len(sub_errors)): 
                next = index+1 if index < len(sub_errors)-1 else -1
                for error in graph.GetEdgesBetween(sub_errors[index], sub_errors[next], all=False): 
                    errors.add(error)
                    
        return self.__MinEdge(graph, errors) if getMinEdges else errors

    def __BFS(self, graph:Graph, node, path, not_visited):
        """BFS algorithm in order to find cycles"""
        errors = []
        #if there is a cycle
        if node in path:
            start_cycle=False

            #we return only the nodes of the cycle
            for index in range(len(path)):
                if path[index]: start_cycle=True
                if start_cycle: errors.append(path[index])
            return errors
        
        path.append(node)

        #foreach adjacent node we apply the recursion
        for adj_node in graph.GetAdj(node):
            if(adj_node in not_visited):
                sub_errors = self.__BFS(graph, adj_node, path, not_visited)
                errors.extend(sub_errors)

        #this node is fully visited
        not_visited.remove(node)
        path.pop()

        return errors

    def __MinEdge(self, graph: Graph, edges):
        """Checks WF with all the permutation of edges to find the minimum required"""
        #we search the minimum number od edges needed to make the graph acyclic
        for index in range(len(edges)-1):
            permutations = itertools.permutations(edges, index+1)
            for permutation in permutations:
                test = deepcopy(graph)
                #remove all the permutations from the graph
                for edge in permutation:
                    test.RemoveEdge(edge)
                #if the graph is acyclic the permutation is the minimum required
                if len(self.Check(test, False))==0:
                    return list(permutation)

    def Apply(self, graph: Graph, errors):
        """Remove WF errors from the graph"""
        for error in errors:
            graph.RemoveEdge(error)

    def ToString(self, errors):
        """Returns the WF errors in a string"""
        string = 'WF - Well-Foundedness:'+'\n'
        if len(errors)==0:
            string += 'WF holds'+'\n'
        else:
            for error in errors:
                string += "- "+EdgeToString(error)+' creates a cycle'+'\n'
        string+='\n'
        return string