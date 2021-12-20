from Graph import Graph

def CheckWF(graph:Graph, errors = None, node = None, visited=None):

        if errors == None: errors = set()
        if visited == None: visited = []
        if node == None: node = graph.startNode

        if node in visited: return False

        visited.append(node)
        for adj_node in graph.GetAdj(node):
            if not CheckWF(graph, errors, adj_node, visited): 
                for label in graph.GetEdgesBetween(node, adj_node, all=False):
                    errors.add((node, label, adj_node, True))

        visited.remove(node)

        return len(errors)==0 if len(visited)==0 else True