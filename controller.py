from graphviz import Source 
import copy
from dot_parser.main import main as parse
from properties.BTI import CheckBTI
from properties.CPI import CheckCPI
from properties.IRE import CheckIRE
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
            if CheckSP(self.graph, err):
                log.append('SP holds')
            else:
                for error in err:
                    start, label, end, is_forward = error
                    if end == None:
                        log.append(start+" should have a "+"forward" if is_forward else "backward" +" transiction labbeled "+label+" to a state")
                    else:
                        log.append('Can\'t find '+EdgeToString(error))

        if properties['BTI'].get():
            log.append('\nBTI - Backward Transitions are Indipendent:')
            err = set()
            if CheckBTI(self.graph, err):
                log.append('BTI holds')
            else:
                for edge1, edge2 in err:
                    log.append(EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent')

        if properties['WF'].get():
            log.append('\nWF - Well-Foundedness:')
            err = set()
            if CheckWF(self.graph, err):
                log.append('WF holds')
            else:
                for error in err:
                    log.append(EdgeToString(error)+' creates a cycle')

        if properties['CPI'].get():
            log.append('\nCPI - Coinitial Propagation of Indipendence:')
            err = set()
            if CheckCPI(self.graph, err):
                log.append('CPI holds')
            else:
                for edge1, edge2 in err:
                    log.append(EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent')

        if properties['IRE'].get():
            log.append('\nIRE - Independence Respects Events:')
            err = set()
            if CheckIRE(self.graph, err):
                log.append('IRE holds')
            else:
                for edge1, edge2 in err:
                    log.append(EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent')

        return log
                
    def generateProperties(self, properties):
        continue_to_check = True
        new_graph = copy.deepcopy(self.graph)
        while continue_to_check:
            continue_to_check = False
            if properties['SP'].get():
                err = []
                if not CheckSP(new_graph, err):
                    continue_to_check = True
                    for error in err:
                        start, label, end, forward = error
                        if(end != None): new_graph.AddEdge(error)
                        
            if properties['BTI'].get():
                err = set()
                if not CheckBTI(new_graph, err):
                    continue_to_check = True
                    for error in err:
                        edge1, edge2 = error
                        new_graph.AddIndipendence(edge1, edge2)
                        
            if properties['WF'].get():
                err = set()
                if not CheckWF(new_graph, err):
                    continue_to_check = True
                    for error in err:
                        new_graph.RemoveEdge(error)
                        
            if properties['CPI'].get():
                err = set()
                if not CheckCPI(new_graph, err):
                    continue_to_check = True
                    for error in err:
                        edge1, edge2 = error
                        new_graph.AddIndipendence(edge1, edge2)

            if properties['IRE'].get():
                err = set()
                if not CheckIRE(new_graph, err):
                    continue_to_check = True
                    for error in err:
                        edge1, edge2 = error
                        new_graph.AddIndipendence(edge1, edge2)

        return new_graph.ToString()

def EdgeToString(edge):
    start, label, end, is_forward = edge
    sign = '-' if is_forward else '~'
    return start+sign+label+sign+'>'+end