from graphviz import Source 
import copy
from dot_parser.main import main as parse

class Controller:
    path = None
    graph = None

    def setPath(self, path):
        self.path = path
        self.graph = parse(self.path)

    def getGraphImage(self):
        s = Source.from_file(self.path)
        s.render(self.path, format='png',view=False)
        return self.path+'.png'

    def checkProperties(self, properties):
        log = []
        if properties['SP'].get():
            log.append('SP - Square Property:')
            err = []
            self.graph.CheckSP(err)
            if err:
                for error in err:
                    log.append('Can\'t find '+EdgeToString(error))
            else:
                log.append('SP holds')
        if properties['BTI'].get():
            log.append('BTI - Backward Transitions are Indipendent:')
            err = []
            self.graph.CheckBTI(err)
            if err:
                for error in err:
                    edge1, edge2 = error
                    log.append(EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent')
            else:
                log.append('BTI holds')
        if properties['WF'].get():
            log.append('WF - Well-Foundedness:')
            err = []
            self.graph.CheckWF(err)
            if err:
                for error in err:
                    log.append(EdgeToString(error)+' creates a cycle')
            else:
                log.append('WF holds')
        return log
                
    def generateProperties(self, properties):
        log = None
        new_graph = copy.deepcopy(self.graph)
        while log == None or len(log)>0:
            log = []
            if properties['SP'].get():
                err = []
                new_graph.CheckSP(err)
                if err:
                    for error in err:
                        new_graph.AddEdge(error)
                        
            if properties['BTI'].get():
                err = []
                new_graph.CheckBTI(err)
                if err:
                    for error in err:
                        edge1, edge2 = error
                        new_graph.AddIndipendence(edge1, edge2)
                        
            if properties['WF'].get():
                err = []
                new_graph.CheckWF(err)
                if err:
                    for error in err:
                        new_graph.RemoveEdge(error)
                        
        return new_graph.ToString()


def EdgeToString(edge):
    start, label, end, is_forward = edge
    sign = '-' if is_forward else '~'
    return start+sign+label+sign+'>'+end