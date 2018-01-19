from model import DuckModel, FemaleDuckAgent, MaleDuckAgent
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox

# show a simulation of ducks mating
class DuckVisualisation():
    def __init__(self, Model):
        self.Model = Model
        self.t = 0
        self.tickrate = 0.01
        self.halt = True
        self.stats_metric = 'statistic 1'
        plt.ion()

        # give the window a fixed size
        self.fig = plt.figure(figsize=(50,50))

        # create a simulation and a statistics plot
        self.sim_ax = self.fig.add_subplot(121)
        self.stats_ax = self.fig.add_subplot(122)

        # let the plot go to half the height and use most of window
        plt.subplots_adjust(bottom=0.55, top=0.95, left=0.05, right=0.95)

        # init sim and stat plots
        plot_m, plot_f = self.init_sim()
        self.init_stats()

        plt.show()

        # keep the window open for eternity
        while True:
            self.run(plot_m, plot_f)
            # run terminated, halt it again
            self.halt = True
            # wait a bit to run again
            plt.pause(0.2)

    # initialize the left side of the figure
    def init_sim(self):
        # set the axis domains
        self.sim_ax.set_xlim(0,100)
        self.sim_ax.set_ylim(0,100)

        # the data to plot
        plot_m, = self.sim_ax.plot([], [], 'o', color='b')
        plot_f, = self.sim_ax.plot([], [], 'o', color='pink')

        # parameters for creating sliders
        self.slider_height = 0.03
        self.slider_bot = 0.05
        self.slider_total = 0

        # create a slider for the tickrate
        tick_pos = plt.axes(self.get_new_slider_pos())
        # valfmt sets the number of decimal places to be shown
        self.tick_slider = Slider(tick_pos, 'Tickrate', 0.0, 0.1, valinit=self.tickrate, valfmt='%1.5f')
        self.tick_slider.on_changed(self.tick_update)

        slider2_pos = plt.axes(self.get_new_slider_pos())
        # valfmt sets the number of decimal places to be shown
        self.slider2 = Slider(slider2_pos, 'Tickrate', 0.0, 0.1, valinit=self.tickrate, valfmt='%1.5f')
        self.slider2.on_changed(self.tick_update)

        # add pause/unpause button
        pause_pos = plt.axes([0.1, 0.0125, 0.1, 0.02])
        self.pause_button = Button(pause_pos, 'Pause/Unpause', color='b', hovercolor='royalblue')
        self.pause_button.on_clicked(self.pause_unpause)

        # add reset button
        reset_pos = plt.axes([0.3, 0.0125, 0.1, 0.02])
        self.reset_button = Button(reset_pos, 'Reset', color='r', hovercolor='orangered')
        self.reset_button.on_clicked(self.reset)

        # textboxje
        box_pos = plt.axes([0.1, 0.2, 0.1, 0.075])
        self.text_box = TextBox(box_pos, 'num_males', initial="10")
        self.text_box.on_submit(self.submit)

        # do a single step to show the model at start
        self.sim_step(plot_m, plot_f)

        return plot_m, plot_f

    # initialize the right side of the figure
    def init_stats(self):
        # create different metrics to show on plot
        metric_ax = plt.axes([0.6, 0.1, 0.3, 0.3])
        self.metric_buttons = RadioButtons(metric_ax, ('statistic 1', 'statistic 2', 'statistic 3'), active=0)
        self.metric_buttons.on_clicked(self.metric_update)

        # do a single step to show the stats at the start
        self.stats_step()

    # plots the ducks (male/female) movement at a given tickrate (speed)
    def run(self, plot_m, plot_f, t_max=5000):
        while self.t < t_max and not self.halt:
            # take a step in the model and in the visualisation
            self.Model.step()
            self.sim_step(plot_m, plot_f)
            self.stats_step()

            # wait for set tickrate
            plt.pause(self.tickrate)

            # increment the time
            self.t += 1

    # do 1 simulation step
    def sim_step(self, plot_m, plot_f):
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

        # show the time as a title
        self.sim_ax.set_title('Step: ' + str(self.t))
        plt.draw()

    # do 1 statistics step
    def stats_step(self):
        # show the metric as the title
        self.stats_ax.set_title(self.stats_metric)

    # gives the position of a newly added slider
    def get_new_slider_pos(self):
        y = self.slider_bot + (self.slider_total * (self.slider_height + self.slider_height/2.0))
        self.slider_total += 1
        return [0.1, y, 0.3, self.slider_height]


    ########################################################################
    # FOLLOWING are listener functions that wait for an update to a widget #

    # take the new slider value
    def tick_update(self, val):
        self.tickrate = val

    # pause if simulation is running,
    # unpause if simulation is halted
    def pause_unpause(self, event):
        if self.halt:
            self.halt = False
            # self.pause_button.label = 'Pause'
        else:
            self.halt = True
            # self.pause_button.label = 'Unpause'

    # reset the model with new parameters
    def reset(self, event):
        self.halt = True
        self.t = 0
        self.init_sim()

    # changes the statistic metric based on a buttonpress
    def metric_update(self, label):
        self.stats_metric = label
        self.stats_ax.set_title(self.stats_metric)

    # voor textboxje
    def submit(self, value):
        self.Model.num_males = int(value)
        self.Model.create_ducks()


if __name__ == '__main__':
    Model = DuckModel(10, 10, 100, 100)

    Vis = DuckVisualisation(Model)
