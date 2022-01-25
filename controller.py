from PIL.Image import FASTOCTREE
from graphviz import Source 
import copy
from Graph import EdgeToString
from dot_parser.main import main as parse
from properties.BTI import CheckBTI
from properties.CPI import CheckCPI
from properties.IRE import CheckIRE
from properties.SP import CheckSP
from properties.WF import CheckWF

class Controller:
    path = None
    graph = None

    def Parse(self, path):
        """Set path oh the file to be read and parse the graph"""
        self.path = path
        graph, errors = parse(self.path)
        self.graph = graph
        return errors

    def GetGraphImage(self):
        """Save graph image and the return path to image"""
        s = Source.from_file(self.path)
        s.render(self.path, format='png',view=False)
        return self.path+'.png'

    def CheckProperties(self, properties):
        """Check graph properties and print error log"""
        errors = {}
        if properties['SP'].get():
            errors['SP']=CheckSP(self.graph, errors['SP'])

        if properties['BTI'].get():
            errors['BTI']=CheckBTI(self.graph, errors['BTI'])

        if properties['WF'].get():
            errors['WF']=CheckWF(self.graph, errors['WF'])

        if properties['CPI'].get():
            errors['CPI']=CheckCPI(self.graph, errors['CPI'])
        
        if properties['IRE'].get():
            errors['IRE']=CheckIRE(self.graph, errors['IRE'])

        return self.ErrorsToString(errors), errors
                
    def ErrorsToString(self, errors):
        log = ""
        if 'SP' in errors:
            log = log + 'SP - Square Property:'+'\n'
            if len(errors['SP'])==0:
                log = log + 'SP holds'+'\n'
            else:
                for ind1, ind2, error in errors['SP']:
                    start, label, end, is_forward = error
                    if end == None:
                        log = log + '- ' + EdgeToString(ind1)+" ι "+EdgeToString(ind2)+" but they don't have any valid t' or u'"
                        #log = log + "- "+start+" should have a "+"forward" if is_forward else "backward" +" transiction labbeled "+label+" to a state"+'\n'
                    else:
                        log = log + '- ' + EdgeToString(ind1)+" ι "+EdgeToString(ind2)+ ' but they don\'t have common end, could be added '+EdgeToString(error)+'\n'

        if 'BTI' in errors:
            log = log + '\nBTI - Backward Transitions are Indipendent:'+'\n'
            if len(errors['BTI'])==0:
                log = log + 'BTI holds'+'\n'
            else:
                for edge1, edge2 in errors['BTI']:
                    log = log + "- "+EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent'+'\n'

        if 'WF' in errors:
            log = log + '\nWF - Well-Foundedness:'+'\n'
            if len(errors['WF'])==0:
                log = log + 'WF holds'+'\n'
            else:
                for error in errors['WF']:
                    log = log + "- "+EdgeToString(error)+' creates a cycle'+'\n'

        if 'CPI' in errors:
            log = log + '\nCPI - Coinitial Propagation of Indipendence:'+'\n'
            if len(errors['CPI'])==0:
                log = log + 'CPI holds'+'\n'
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
                
                log = log + (ltsi_error if print_error else missing_indipendence)+'\n'

        if 'IRE' in errors:
            log = log + '\nIRE - Independence Respects Events:'+'\n'
            if len(errors['IRE'])==0:
                log = log + 'IRE holds'+'\n'
            else:
                for ind, edge1, edge2 in errors['IRE']:
                    log = log + "- "+EdgeToString(edge1)+" ~ "+EdgeToString(ind)+" ι "+EdgeToString(edge2)+" but "+EdgeToString(edge1)+' and '+EdgeToString(edge2)+' are not indipendent'+'\n'
        
        return log

    def ForceProperties(self, errors):
        """Check graph properties and return a new graph with the selected properties in DOT format"""
        new_graph = copy.deepcopy(self.graph)
        if 'SP' in errors:
            for ind1, ind2, error in errors['SP']:
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
            for ev, edge1, edge2 in errors['IRE']:
                new_graph.AddIndipendence(edge1, edge2)

        return new_graph.ToString()