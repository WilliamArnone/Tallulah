from PIL.Image import FASTOCTREE
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
        """Set path oh the file to be read and parse the graph"""
        self.path = path
        graph, errors = parse(self.path)
        self.graph = graph
        return errors

    def getGraphImage(self):
        """Save graph image and the return path to image"""
        s = Source.from_file(self.path)
        s.render(self.path, format='png',view=False)
        return self.path+'.png'

    def checkProperties(self, properties):
        """Check graph properties and print error log"""
        log = []
        errors = {}
        if properties['SP'].get():
            errors['SP']=set()
            log.append('SP - Square Property:')
            if CheckSP(self.graph, errors['SP']):
                log.append('SP holds')
            else:
                for error in errors['SP']:
                    start, label, end, is_forward = error
                    if end == None:
                        log.append("- "+start+" should have a "+"forward" if is_forward else "backward" +" transiction labbeled "+label+" to a state")
                    else:
                        log.append('- Can\'t find '+EdgeToString(error))

        if properties['BTI'].get():
            errors['BTI']=set()
            log.append('\nBTI - Backward Transitions are Indipendent:')
            if CheckBTI(self.graph, errors['BTI']):
                log.append('BTI holds')
            else:
                for edge1, edge2 in errors['BTI']:
                    log.append("- "+EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent')

        if properties['WF'].get():
            errors['WF']=set()
            log.append('\nWF - Well-Foundedness:')
            if CheckWF(self.graph, errors['WF']):
                log.append('WF holds')
            else:
                for error in errors['WF']:
                    log.append("- "+EdgeToString(error)+' creates a cycle')

        if properties['CPI'].get():
            errors['CPI']=set()
            log.append('\nCPI - Coinitial Propagation of Indipendence:')
            if CheckCPI(self.graph, errors['CPI']):
                log.append('CPI holds')
            else:
                missing_indipendence = ""
                ltsi_error = "CLOSURE UNDER CPI CANNOT BE PERFORMED!"
                print_error = False
                for edge1, edge2, rev, edge in errors['CPI']:
                    if rev == edge:
                        print_error = True
                        ltsi_error = ltsi_error + "\n- The relation "+EdgeToString(edge1)+" ι "+EdgeToString(edge2)+" would imply "+EdgeToString(rev)+" ι "+EdgeToString(edge)+", but this is not possible since independence is irreflexive"
                    else:
                        missing_indipendence = missing_indipendence + "\n- " + EdgeToString(edge1)+' ι '+EdgeToString(edge2)+' but '+EdgeToString(rev)+" and "+EdgeToString(edge)+ " are not"
                
                log.append(ltsi_error if print_error else missing_indipendence)

        if properties['IRE'].get():
            errors['IRE']=set()
            log.append('\nIRE - Independence Respects Events:')
            if CheckIRE(self.graph, errors['IRE']):
                log.append('IRE holds')
            else:
                for edge1, edge2 in errors['IRE']:
                    log.append("- "+EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent')

        return log, errors
                
    def generateProperties(self, graph, errors):
        """Check graph properties and return a new graph with the selected properties"""
        new_graph = copy.deepcopy(graph)
        if 'SP' in errors:
            for error in errors['SP']:
                start, label, end, forward = error
                if(end != None): new_graph.AddEdge(error)
                        
        if 'BTI' in errors:
            for error in errors['BTI']:
                edge1, edge2 = error
                new_graph.AddIndipendence(edge1, edge2)
                        
        if 'WF' in errors:
            for error in errors['WF']:
                new_graph.RemoveEdge(error)
                        
        if 'CPI' in errors:
            for error in errors['CPI']:
                edge1, edge2, rev, edge = error
                if rev != edge: new_graph.AddIndipendence(rev, edge)

        if 'IRE' in errors:
            for error in errors['IRE']:
                edge1, edge2 = error
                new_graph.AddIndipendence(edge1, edge2)

        return new_graph.ToString()
    
    def GetIndipendenceString(self):
        """Return indipendece between transition in a printable string"""
        text = ""
        for indipendence in self.graph.indipendence:
            edge1, edge2 = indipendence
            text = text+EdgeToString(edge1)+" ι "+EdgeToString(edge2)+"\n"
        return text


def EdgeToString(edge):
    """Return a printable string of an edge"""
    start, label, end, is_forward = edge
    sign = '-' if is_forward else '~'
    return start+sign+label+sign+'>'+end