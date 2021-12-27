from Graph import Graph

#No infinite reverse computation
#we do not have Pi:= Pi+1-αi->Pi for all i = 0,1,...
def CheckWF(graph:Graph, errors:set = None, node = None, visited = None):
    """Check WF property and return true if holds"""
    #a dot file is finite, the only way to make infinite paths is to make a cycle
    #initialize variables
    if errors == None: errors = set()
    if visited == None: visited = []
    if node == None: node = graph.startNode

    #found an already visited node
    if node in visited: return False

    visited.append(node)
    for adj_node in graph.GetAdj(node):
        if not CheckWF(graph, errors, adj_node, visited): 
            for edge in graph.GetEdgesBetween(node, adj_node, all=False):
                errors.add(edge)

    visited.remove(node)

    #we return true while visiting the graph because we want to find wich edge creates a cycle
    #we don't want to stop at the first cycle found
    return len(errors)==0 if len(visited)==0 else True