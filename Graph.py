from gettext import translation
from random import randint
class Graph:
    #to save memory, edges are saved as an item in a list of labels, in a dictionary with keys (node1, node2)
    #functions return edges in the format (start, label, end, is_forward) 
    
    colors_default = ['#bfef45',
        '#800000',
        '#000075',
        '#42d4f4',
        '#7698B3',
        '#aaffc3',
        '#ffe119',
        '#808000',
        '#008080',
        '#f58231',
        '#023C40',
        '#dcbeff',
        '#469990',
        '#3cb44b',
        '#481620',
        '#DE3163']
    
    def __init__(self):
        #initialize all variables
        self.edges = {}
        self.events = []
        self.nodes = set()
        self.indipendence = set()

    def AddNode(self, *nodes):
        """Add node to the set of nodes"""
        for node in nodes: self.nodes.add(node)

    def AddEdge(self, edge):
        """Add labelled edge to the graph"""
        lst = list(edge)
        start = lst[0] 
        label = lst[1]
        end = lst[2]

        #edge can be in the form (start, label, end) or (start, label, end, is_forward)
        is_forward = len(lst)==3 or lst[3]
        self.AddNode(start, end)
        
        #we save only the forward transitions
        if not is_forward: start, end = end, start
        if not (start, end) in self.edges: 
            self.edges[(start, end)] = []
        if not label in self.edges[(start, end)]:
            self.edges[(start, end)].append(label)

        new_event = set()
        new_event.add((start, label, end, True))
        self.events.append(new_event)
        new_event = set()
        new_event.add((end, label, start, False))
        self.events.append(new_event)

    def RemoveEdge(self, edge):
        """Remove edge from graph"""
        lst = list(edge)
        start = lst[0] 
        label = lst[1]
        end = lst[2]
        
        #edge can be in the form (start, label, end) or (start, label, end, is_forward)
        is_forward = len(lst)==3 or lst[3]
        if not is_forward: start, end = end, start
        if (start, end) in self.edges:
            self.edges[(start, end)].remove(label)

        #we remove all the indipendences wich have the removed edge
        for edge1, edge2 in self.indipendence:
            if edge == edge2 or edge == edge1 or ReverseEdge(edge) == edge2 or ReverseEdge(edge) == edge1: 
                self.indipendence.remove((edge1, edge2))

    def GetEdgesFrom(self, node, all=True, only_forward=True):
        """Return forward, backward or both transitions from input node"""
        edges = []
        for end in self.nodes:
            if (node, end) in self.edges:
                forward = self.edges[(node, end)]
                for label in forward:
                    if all or only_forward: edges.append((node, label, end, True))
            if (end, node) in self.edges:
                backward = self.edges[(end, node)]
                for label in backward:
                    if all or not only_forward: edges.append((node, label, end, False))

        return edges

    def GetEdgesBetween(self, start, end, all=True, only_forward=True):
        """Return forward, backward or both transitions from start to end"""
        edges = []
        if all or only_forward:
            labels = self.edges[(start,end)] if (start, end) in self.edges else []
            for label in labels: edges.append((start, label, end, True))
        if all or not only_forward:
            labels = self.edges[(end,start)] if (end, start) in self.edges else []
            for label in labels: edges.append((start, label, end, False))

        return edges
    
    def EdgeExists(self, edge):
        """Return true if the input edge exists"""
        start, label, end, forward = edge
        if not forward: start, end = end, start
        return label in self.edges[(start, end)] if (start, end) in self.edges else False

    def GetAdj(self, node):
        """Return all nodes reachable from the input node using forward transitions"""
        nodes = []
        for end in self.nodes:
            if (node, end) in self.edges and self.edges[(node, end)]:
                nodes.append(end)

        return nodes

    def AddIndipendence(self, edge1, edge2):
        """Add indipendence between two input nodes"""
        if not (edge2, edge1) in self.indipendence:
            if edge1!=edge2: self.indipendence.add((edge1, edge2))

    def AreIndipendent(self, edge1, edge2):
        """Return true if the transitions are indipendent"""
        for i in self.indipendence:
            if i == (edge1, edge2) or i == (edge2, edge1):
                return True
        return False

    def InitEvents(self):
        """Initialize event classes"""
        temp = []
        for edge1, edge2 in self.indipendence: 
            if not self.EdgeExists(edge1) or not self.EdgeExists(edge2) : temp.append((edge1, edge2))
        for indipendence in temp: self.indipendence.remove(indipendence)

        for start in self.nodes:
            edges = self.GetEdgesFrom(start)

            for edge1 in edges:
                (start1, label1, end1, is_forward1) = edge1
                for edge2 in edges:
                    #if edge1 == edge2: continue

                    (start2, label2, end2, is_forward2) = edge2
                    
                    for end in self.nodes:
                        first = (end1, label2, end, is_forward2)
                        second = (end2, label1, end, is_forward1)

                        # searching for diamonds
                        if self.EdgeExists(first) and self.EdgeExists(second):
                            # we check if there is indipendence at each angle 
                            cond = {(edge1, edge2),
                                (ReverseEdge(edge1), first),
                                (ReverseEdge(edge2), second),
                                (ReverseEdge(first), ReverseEdge(second))
                            }

                            indipendent = True
                            for condition in cond:
                                ind1, ind2 = condition
                                indipendent = indipendent and self.AreIndipendent(ind1, ind2)
                            
                            # last condition of the event definition
                            if indipendent and ((is_forward1 == is_forward2 and end1 != end2) or (is_forward1 == is_forward2 and start != end)):
                                    self.AddToEvent(edge1, second)
                                    self.AddToEvent(edge2, first)

    def AddToEvent(self, edge1, edge2):
        """Union between events of two input transitions"""
        union = set()
        event1 = None
        event2 = None
        
        for event in self.events:
            # we make an union between their event class
            if edge1 in event: 
                event1 = event
                union = union.union(event)
            if edge2 in event: 
                event2 = event
                union = union.union(event)

        # we remove the previous event stored, if any
        if (event1 != None): self.events.remove(event1) 
        else: union.add(edge1)
        if (event2 != None and event2 != event1): self.events.remove(event2)
        else: union.add(edge2)
        self.events.append(union)

    def GetEventClass(self, edge):
        """Return the event class of the input edge"""
        for event in self.events:
            if edge in event: return event

    def ToString(self, color_events=True):
        """Return the graph as a string"""

        self.InitEvents()
        graph = 'digraph G {\n'

        colors = []
        n_events = len(self.events)

        #creates random colors
        for i in range(n_events):
            colors.append('#%06X' % randint(0, 0xFFFFFF))

        for i in range(min(len(colors), len(self.colors_default))):
            colors[i]=self.colors_default[i]


        #first 16 colors are not random
        for start in self.nodes:
            for end in self.nodes:
                if not (start, end) in self.edges: continue
                for label in self.edges[(start, end)]:

                    #we don't want to use colors for backward events
                    backward_counter = 0

                    for i in range(n_events):
                        transition = list(list(self.events[i])[0])
                        if(not transition[3]): backward_counter = backward_counter + 1
                        if (start, label, end, True) in self.events[i]: break
                    graph = graph + '\t"' + start + '" -> "' + end +'" [label="'+label+'", color="'+colors[i-backward_counter]+'"]\n'
        
        graph = graph + "} \n /* \n"
        
        for (start1, label1, end1, is_forward1), (start2, label2, end2, is_forward2) in self.indipendence:
            graph = graph + '\t' + ('> ' if is_forward1 else '< ') + start1 + ' -' + label1 + '-> '+ end1 +' / '
            graph = graph + ('> ' if is_forward2 else '< ') + start2 + ' -' + label2 + '-> '+ end2 +'\n'

        graph = graph + '*/'
        return graph
       
    def GetIndipendenceString(self):
        """Return indipendece between transition in a printable string"""
        text = ""
        for indipendence in self.indipendence:
            edge1, edge2 = indipendence
            text = text+EdgeToString(edge1)+" ι "+EdgeToString(edge2)+"\n"
        return text

def ReverseEdge(edge):
        """Return the reverse transition of the input"""
        start, label, end, is_forward = edge
        return (end, label, start, not is_forward)

def EdgeToString(edge):
    """Return a printable string of an edge"""
    start, label, end, is_forward = edge
    sign = '-' if is_forward else '~'
    return start+sign+label+sign+'>'+end