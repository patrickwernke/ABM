from model import DuckModel, FemaleDuckAgent, MaleDuckAgent
import matplotlib.pyplot as plt
from pycx_gui import GUI

if __name__ == '__main__':
    models = DuckModel(10, 10, 100, 100)

    cx = GUI(models)
    cx.start()
