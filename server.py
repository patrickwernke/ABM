# Adapted from the tutorial
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from duckmodel import DuckModel, FemaleDuckAgent
from HistModule import HistogramModule

WIDTH = 2
HEIGHT = 2

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


    
grid = CanvasGrid(duck_portrayal, WIDTH, HEIGHT, 500, 500)
histogram = HistogramModule(list(range(1,21)), 200, 500)

model_args = {'N':2, 'width':WIDTH, 'height':HEIGHT}
server = ModularServer(DuckModel, [grid, histogram], 'Mating of ducks', model_args)
