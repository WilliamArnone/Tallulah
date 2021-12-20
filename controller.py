from graphviz import Source 
import copy
from dot_parser.Graph import Graph
from dot_parser.main import main as parse

class Controller:
    path = None
    graph = None

    def setPath(self, path):
        self.path = path
        graph, errors = parse(self.path)
        self.graph = graph
        return errors

    def getGraphImage(self):
        s = Source.from_file(self.path)
        s.render(self.path, format='png',view=False)
        return self.path+'.png'

    def checkProperties(self, properties):
        log = []
        if properties['SP'].get():
            log.append('SP - Square Property:')
            err = set()
            self.CheckSP(self.graph, err)
            if err:
                for error in err:
                    start, label, end, is_forward = error
                    if end == None:
                        log.append(start+" should have a transiction labbeled "+label+" to a state")
                    else:
                        log.append('Can\'t find '+EdgeToString(error))
            else:
                log.append('SP holds')

        if properties['BTI'].get():
            log.append('BTI - Backward Transitions are Indipendent:')
            err = set()
            self.CheckBTI(self.graph, err)
            if err:
                for edge1, edge2 in err:
                    log.append(EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent')
            else:
                log.append('BTI holds')

        if properties['WF'].get():
            log.append('WF - Well-Foundedness:')
            err = set()
            self.CheckWF(self.graph, err)
            if err:
                for error in err:
                    log.append(EdgeToString(error)+' creates a cycle')
            else:
                log.append('WF holds')

        if properties['CPI'].get():
            log.append('CPI - Coinitial Propagation of Indipendence:')
            err = set()
            self.CheckCPI(self.graph, err)
            if err:
                for edge1, edge2 in err:
                    log.append(EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent')
            else:
                log.append('CPI holds')

        return log
                
    def generateProperties(self, properties):
        log = None
        new_graph = copy.deepcopy(self.graph)
        while log == None or len(log)>0:
            log = []
            if properties['SP'].get():
                err = []
                self.CheckSP(new_graph, err)
                if err:
                    for error in err:
                        start, label, end, forward = error
                        if(end != None): new_graph.AddEdge(error)
                        
            if properties['BTI'].get():
                err = set()
                self.CheckBTI(new_graph, err)
                if err:
                    for error in err:
                        edge1, edge2 = error
                        new_graph.AddIndipendence(edge1, edge2)
                        
            if properties['WF'].get():
                err = set()
                self.CheckWF(new_graph, err)
                if err:
                    for error in err:
                        new_graph.RemoveEdge(error)
                        
            if properties['CPI'].get():
                err = set()
                self.CheckCPI(new_graph, err)
                if err:
                    for error in err:
                        edge1, edge2 = error
                        new_graph.AddIndipendence(edge1, edge2)

        return new_graph.ToString()

    def CheckWF(self, graph:Graph, errors = None, node = None, visited=None):

        if errors == None: errors = set()
        if visited == None: visited = []
        if node == None: node = graph.startNode

        if node in visited: return False

        visited.append(node)
        for adj_node in graph.GetAdj(node):
            if not self.CheckWF(graph, errors, adj_node, visited): 
                for label in graph.GetEdgesBetween(node, adj_node, all=False):
                    errors.add((node, label, adj_node, True))

        visited.remove(node)

        return len(errors)==0 if len(visited)==0 else True


    def CheckSP(self, graph:Graph, errors = None):
        if errors == None: errors = set()
        for node in graph.nodes:
            #remove all=False to check also backward transitions
            edges = graph.GetEdgesFrom(node, all=False)
            for edge1 in edges:
                (start1, label1, end1, is_forward1) = edge1
                for edge2 in edges:
                    (start2, label2, end2, is_forward2) = edge2
                    if graph.AreIndipendent(edge1, edge2):
                        found = False
                        firstForward = is_forward1 if (is_forward1==is_forward2) else not is_forward1
                        secondForward = is_forward2 if (is_forward1==is_forward2) else not is_forward2
                        for s in graph.nodes:
                            first_start, first_end = (end1, s) if firstForward else (s, end1)
                            second_start, second_end = (end2, s) if secondForward else (s, end2)

                            first = (first_start, label2, first_end, firstForward)
                            second = (second_start, label1, second_end, secondForward)

                            firstExist = graph.EdgeExists(first) 
                            secondExist = graph.EdgeExists(second)

                            if firstExist or secondExist:
                                found = True
                                if not firstExist:
                                    errors.add((end1, label2, s, firstForward))
                                elif not secondExist:
                                    errors.add((end2, label1, s, secondForward))

                        if not found:
                            errors.add((end1, label2, None, firstForward))
                            errors.add((end2, label1, None, secondForward))

                        
        return len(errors)==0

    def CheckBTI(self, graph:Graph, errors = None):
        if errors == None: errors = set()
        for node in graph.nodes:
            edges = graph.GetEdgesFrom(node, all=False, only_forward=False)
            for edge1 in edges:
                for edge2 in edges:
                    if edge1 != edge2 and not graph.AreIndipendent(edge1, edge2):
                        errors.add((edge1, edge2))
        return len(errors)==0

    def CheckCPI(self, graph:Graph, errors):
        if errors == None: errors = set()
        for node in graph.nodes:
            edges = graph.GetEdgesFrom(node, all=False)
            for edge1 in edges:
                (start1, label1, end1, is_forward1) = edge1
                for edge2 in edges:
                    #is this necessary?
                    if edge1 == edge2: continue

                    (start2, label2, end2, is_forward2) = edge2
                    for s in graph.nodes:
                        firstExist = graph.EdgeExists((end1, label2, s, True))
                        secondExist = graph.EdgeExists((end2, label1, s, True))

                        if firstExist and secondExist:
                            cond = []
                            temp = []
                            cond.append((edge1, edge2))
                            cond.append(((end1, label1, start1, False), 
                                (end1, label2, s, True)))
                            cond.append(((end2, label2, start2, False), 
                                (end2, label1, s, True)))
                            cond.append(((s, label2, end1, False), 
                                (s, label1, end2, False)))

                            for condition in cond:
                                first, second = condition
                                if not graph.AreIndipendent(first, second): temp.append(condition)

                            if len(temp) > 0 and len(temp) < 4:
                                for condition in temp:
                                    errors.add(condition)
                        
        return len(errors)==0


def EdgeToString(edge):
    start, label, end, is_forward = edge
    sign = '-' if is_forward else '~'
    return start+sign+label+sign+'>'+end