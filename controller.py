from PIL.Image import FASTOCTREE
from graphviz import Source 
import copy
from Graph import EdgeToString
from dot_parser.main import main as parse
from properties.BTI import BTI
from properties.CPI import CPI
from properties.IRE import IRE
from properties.SP import SP
from properties.WF import WF

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
            errors['SP']=SP.Check(self.graph)

        if properties['BTI'].get():
            errors['BTI']=BTI.Check(self.graph)

        if properties['WF'].get():
            errors['WF']=WF.Check(self.graph)

        if properties['CPI'].get():
            errors['CPI']=CPI.Check(self.graph)
        
        if properties['IRE'].get():
            errors['IRE']=IRE.Check(self.graph)

        return self.ErrorsToString(errors), errors
                
    def ErrorsToString(self, errors):
        log = ""
        if 'SP' in errors:
            log += SP.ToString(errors['SP'])

        if 'BTI' in errors:
            log += BTI.ToString(errors['BTI'])

        if 'WF' in errors:
            log += WF.ToString(errors['WF'])

        if 'CPI' in errors:
            log += CPI.ToString(errors['CPI'])

        if 'IRE' in errors:
            log += IRE.ToString(errors['IRE'])
        
        return log

    def ForceProperties(self, errors):
        """Check graph properties and return a new graph with the selected properties in DOT format"""
        new_graph = copy.deepcopy(self.graph)
        if 'SP' in errors:
            SP.Apply(new_graph, errors['SP'])
                        
        if 'BTI' in errors:
            BTI.Apply(new_graph, errors['BTI'])
                        
        if 'WF' in errors:
            WF.Apply(new_graph, errors['WF'])
                        
        if 'CPI' in errors:
            CPI.Apply(new_graph, errors['CPI'])

        if 'IRE' in errors:
            IRE.Apply(new_graph, errors['CPI'])

        return new_graph.ToString()