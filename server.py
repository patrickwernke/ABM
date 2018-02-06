# Adapted from the tutorial
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from duckmodel import DuckModel, FemaleDuckAgent
from HistModule import HistogramModule
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

WIDTH = 50
HEIGHT = 50

def duck_portrayal(duck):
    """ Information about the agents for the animation. """

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

# Sliders
number_agent = UserSettableParameter("slider", "Number of agents", 20, 1, 100, 1)
season_length = UserSettableParameter("slider", "length of season", 20, 10, 50, 1)
mutation = UserSettableParameter("slider", "Mutation chance", 0.1, 0, 1, 0.05)
partner_egg = UserSettableParameter("slider", "# partner mating", 20, 10, 50, 1)
base_succes_mate = UserSettableParameter("slider", "Base success chance of mating", 0.25, 0, 1, 0.05)

# Graphs
histogram = HistogramModule(list(range(1,21)), 200, 500)
grid = CanvasGrid(duck_portrayal, WIDTH, HEIGHT, 500, 500)

# Model arguments and server setup.
model_args = {'N':number_agent, 'width':WIDTH, 'height':HEIGHT, "season_length": season_length,
                "mutation": mutation, "partner_egg": partner_egg, "base_succes_mate": base_succes_mate}
server = ModularServer(DuckModel, [grid, histogram], 'DuckModel', model_args)
