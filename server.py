# Adapted from the tutorial
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import DuckModel

def duck_portrayal(duck):
    attributes = {'Shape': 'circle',
                  'Filled': 'true',
                  'Layer': 0,
                  'Color': 'red',
                  'r': 0.5}
    return attributes

grid = CanvasGrid(duck_portrayal, 10, 10, 500, 500)

model_args = {'N_female':10, 'N_male':10, 'width':100, 'height':100}
server = ModularServer(DuckModel, [grid], 'Mating of ducks', model_args)