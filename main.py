# model.py
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
        self.grid = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        # Create agents
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

if __name__ == '__main__':
    model = DuckModel(10, 10, 100, 100)
    
    plt.ion()
    fig=plt.figure()
    ax=fig.add_subplot(111)
    xs = []
    ys = []
    for agent in model.schedule.agents:
        xs.append(agent.pos[0])
        ys.append(agent.pos[1])    
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    plot, = ax.plot(xs, ys, 'o')
    
    for i in range(200):
        model.step()
        xs = []
        ys = []
        for agent in model.schedule.agents:
            xs.append(agent.pos[0])
            ys.append(agent.pos[1])
        plot.set_xdata(xs)
        plot.set_ydata(ys)
        plt.draw()
        plt.pause(0.05)
        plt.show()