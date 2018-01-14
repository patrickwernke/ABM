from mesa.space import ContinuousSpace
from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np
import matplotlib.pyplot as plt

class DuckModel(Model):
    """A model with some number of agents."""
    def __init__(self, N_female, N_male, width, height):
        self.num_females = N_female
        self.num_males = N_male
        self.params = ("num_females", "num_males")
        self.grid = ContinuousSpace(width, height, True)
        # Create agents
        self.create_ducks()

    def create_ducks(self):
        self.schedule = RandomActivation(self)

        for i in range(self.num_females):
            duck = FemaleDuckAgent(i, self)
            self.schedule.add(duck)
            # Add the agent to a random place
            x = np.random.uniform(self.grid.x_min, self.grid.x_max)
            y = np.random.uniform(self.grid.y_min, self.grid.y_max)
            self.grid.place_agent(duck, (x, y))
        for _ in range(self.num_males):
            i+=1 # keep count from the previous i
            duck = MaleDuckAgent(i, self)
            self.schedule.add(duck)
            x = np.random.uniform(self.grid.x_min, self.grid.x_max)
            y = np.random.uniform(self.grid.y_min, self.grid.y_max)
            self.grid.place_agent(duck, (x, y))

    def step(self):
        self.schedule.step()

    def reset(self):
        self.create_ducks()

    def startdraw(self):
        self.fig=plt.figure()
        ax=self.fig.add_subplot(111)

        ax.set_xlim(0,100)
        ax.set_ylim(0,100)
        self.plot_m, = ax.plot([], [], 'o', color='b')
        self.plot_f, = ax.plot([], [], 'o', color='r')

    def draw(self):
        x_m = []
        y_m = []
        x_f = []
        y_f = []

        for agent in self.schedule.agents:
            if isinstance(agent, FemaleDuckAgent):
                x_f.append(agent.pos[0])
                y_f.append(agent.pos[1])
            else:
                x_m.append(agent.pos[0])
                y_m.append(agent.pos[1])

        self.plot_m.set_ydata(y_m)
        self.plot_m.set_xdata(x_m)
        self.plot_f.set_ydata(y_f)
        self.plot_f.set_xdata(x_f)

        #plt.draw()

class DuckAgent(Agent):
    """ An agent (a duck) with random speed."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.speed = np.random.uniform(0.5,3)

    def move(self):
        angle = np.random.uniform(0, 2*np.pi)
        distance = np.random.uniform(0,self.speed)

        x=self.pos[0]
        y=self.pos[1]
        newx = x + distance * np.cos(angle)
        newy = y + distance * np.sin(angle)
        new_position = (newx,newy)

        self.model.grid.move_agent(self, self.model.grid.torus_adj(new_position))

    def step(self):
        self.move()

class FemaleDuckAgent(DuckAgent):
    pass

class MaleDuckAgent(DuckAgent):
    pass
