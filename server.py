# Adapted from the tutorial
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from duckmodel import DuckModel, FemaleDuckAgent

def duck_portrayal(duck):
    if isinstance(duck, FemaleDuckAgent):
        c = 'red'
    else:
        c = 'blue'

    attributes = {'Shape': 'circle',
                  'Filled': 'true',
                  'Layer': 0,
                  'Color': c,
                  'r': 0.5}
    return attributes

grid = CanvasGrid(duck_portrayal, 50, 50, 500, 500)

model_args = {'N':3, 'width':50, 'height':50}
server = ModularServer(DuckModel, [grid], 'Mating of ducks', model_args)