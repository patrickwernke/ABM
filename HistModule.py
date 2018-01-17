from mesa.visualization.ModularVisualization import VisualizationElement
from duckmodel import MaleDuckAgent
import numpy as np

class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})".format(bins, 
                                                               canvas_width, 
                                                               canvas_height)

        self.js_code = "elements.push(" + new_element + ");"
    
    def render(self, model):
        wealth_vals = [agent.aggression for agent in model.schedule.agents if isinstance(agent, MaleDuckAgent)]
        hist = np.histogram(wealth_vals, bins=self.bins)[0]
        return [int(x) for x in hist]