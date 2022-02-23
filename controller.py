from PIL.Image import FASTOCTREE
from graphviz import Source, render
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
        #this code isn't compatible with previous versions of graphviz
        #s = Source.from_file(self.path)
        #s.render(self.path, format='png',view=False)
        #return self.path+'.png'
        return render('dot', 'png', self.path)

    def CheckProperties(self, properties):
        """Check graph properties and print error log"""
        errors = {}

        for property_id in properties:
            if properties[property_id].get():
                errors[property_id] = self.CheckProperty(property_id)

        return self.graph, errors

    def ForceProperties(self, graph, errors, check_values):
        """Check graph properties and return a new graph with the selected properties in DOT format"""
        new_graph = copy.deepcopy(graph)
        
        for property_id in errors:
            for i in range(len(errors[property_id])): 
                if(check_values[property_id][i].get()):
                    self.ForceProperty(new_graph, property_id, errors[property_id][i])

        return new_graph

    def GetPropertyName(self, property_id):
        """Return the complete property name given its id"""
        return self.GetPropertyByID(property_id).name

    def CheckProperty(self, property_id):
        """Check the property and returns the errors if any"""
        return self.GetPropertyByID(property_id).Check(self.graph)

    def GetLog(self, property_id, error):
        """Return the error in a list of (text, color)"""
        return self.GetPropertyByID(property_id).GetLog(error)

    def IsErrorApplyable(self, property_id, error):
        """Return True if the error can be removed"""
        return self.GetPropertyByID(property_id).IsApplyable(error)

    def ForceProperty(self, graph, property_id, error):
        """Remove the error from the graph"""
        if self.IsErrorApplyable(property_id, error):
            self.GetPropertyByID(property_id).Apply(graph, error)

    def GetPropertyByID(self, property_id):
        """Return the the property given its id"""
        if property_id=="SP": return SP
        elif property_id=="WF": return WF
        elif property_id=="BTI": return BTI
        elif property_id=="CPI": return CPI
        elif property_id=="IRE": return IRE
