from graphviz import Source 
import copy
from dot_parser.main import main as parse
from properties.BTI import CheckBTI
from properties.CPI import CheckCPI
from properties.SP import CheckSP
from properties.WF import CheckWF

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
            CheckSP(self.graph, err)
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
            CheckBTI(self.graph, err)
            if err:
                for edge1, edge2 in err:
                    log.append(EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent')
            else:
                log.append('BTI holds')

        if properties['WF'].get():
            log.append('WF - Well-Foundedness:')
            err = set()
            CheckWF(self.graph, err)
            if err:
                for error in err:
                    log.append(EdgeToString(error)+' creates a cycle')
            else:
                log.append('WF holds')

        if properties['CPI'].get():
            log.append('CPI - Coinitial Propagation of Indipendence:')
            err = set()
            CheckCPI(self.graph, err)
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
                CheckSP(new_graph, err)
                if err:
                    for error in err:
                        start, label, end, forward = error
                        if(end != None): new_graph.AddEdge(error)
                        
            if properties['BTI'].get():
                err = set()
                CheckBTI(new_graph, err)
                if err:
                    for error in err:
                        edge1, edge2 = error
                        new_graph.AddIndipendence(edge1, edge2)
                        
            if properties['WF'].get():
                err = set()
                CheckWF(new_graph, err)
                if err:
                    for error in err:
                        new_graph.RemoveEdge(error)
                        
            if properties['CPI'].get():
                err = set()
                CheckCPI(new_graph, err)
                if err:
                    for error in err:
                        edge1, edge2 = error
                        new_graph.AddIndipendence(edge1, edge2)

        return new_graph.ToString()

def EdgeToString(edge):
    start, label, end, is_forward = edge
    sign = '-' if is_forward else '~'
    return start+sign+label+sign+'>'+end