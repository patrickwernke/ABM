from model import DuckModel, FemaleDuckAgent, MaleDuckAgent
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

# show a simulation of ducks mating
class DuckVisualisation():
    def __init__(self, Model):
        self.Model = Model
        self.sliders = {}
        self.tickrate = 0.01
        plt.ion()

        # give the window a fixed size
        fig=plt.figure(figsize=(10,50))

        ax=fig.add_subplot(111)
        # let the plot go to half the height of window
        plt.subplots_adjust(bottom=0.5)
        
        # set the axis domains
        ax.set_xlim(0,100)
        ax.set_ylim(0,100)

        # the data to plot
        plot_m, = ax.plot([], [], 'o', color='b')
        plot_f, = ax.plot([], [], 'o', color='pink')
        plt.show()

        # create a slider for the tickrate
        tick_axes = plt.axes([0.25, 0.1, 0.65, 0.03]) #the position of the slider
        tick_slider = Slider(tick_axes, 'Tickrate', 0.0001, 0.1, valinit=self.tickrate)
        tick_slider.on_changed(self.tick_slider_update)
        self.sliders['Tickrate'] = tick_slider

        self.run(plot_m, plot_f)

    # plots the ducks (male/female) movement at a given tickrate (speed)
    def run(self, plot_m, plot_f, max_iter=5000):
        for i in range(max_iter):
            # take a step in the model and in the visualisation
            self.Model.step()
            self.step(plot_m, plot_f)

            # wait for set tickrate
            plt.pause(self.tickrate)

    # do 1 simulation step
    def step(self, plot_m, plot_f):
        x_m = []
        y_m = []
        x_f = []
        y_f = []
        for agent in Model.schedule.agents:
            if isinstance(agent, FemaleDuckAgent):        
                x_f.append(agent.pos[0])
                y_f.append(agent.pos[1])
            else:
                x_m.append(agent.pos[0])
                y_m.append(agent.pos[1])

        plot_m.set_ydata(y_m)
        plot_m.set_xdata(x_m)
        plot_f.set_ydata(y_f)
        plot_f.set_xdata(x_f)
        
        plt.draw()

    # take the new slider value
    def tick_slider_update(self, val):
        self.tickrate = val


if __name__ == '__main__':
    Model = DuckModel(10, 10, 100, 100)
    
    Vis = DuckVisualisation(Model)
