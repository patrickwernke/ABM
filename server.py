# Adapted from the tutorial
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from duckmodel import DuckModel, FemaleDuckAgent

def duck_portrayal(duck):
    if isinstance(duck, FemaleDuckAgent):
        c = 'red'
        r = 1
        layer=0
    else:
        c = 'blue'
        r = 0.5
        layer=1

    attributes = {'Shape': 'circle',
                  'Filled': 'true',
                  'Layer': layer,
                  'Color': c,
                  'r': r}
    return attributes

grid = CanvasGrid(duck_portrayal, 50, 50, 500, 500)

model_args = {'N':3, 'width':50, 'height':50}
server = ModularServer(DuckModel, [grid], 'Mating of ducks', model_args)