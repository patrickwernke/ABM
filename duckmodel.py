# model.py
from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np

class DuckModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.running=True
        self.ID = 0
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.current_step = 0

        self.duckdic={}

        # Create agents
        for _ in range(self.num_agents):
            m = MaleDuckAgent(self.ID, self.ID+1, random.randint(2, 10), self)
            self.duckdic[self.ID] = m
            self.ID += 1

            f = FemaleDuckAgent(self.ID, self.ID-1, m, self)
            self.duckdic[self.ID] = f
            self.ID += 1

            self.schedule.add(f)
            self.schedule.add(m)

            # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(f, (x, y))
            self.grid.place_agent(m, (x, y))

    def get_duck_by_id(self, ID):
        return self.duckdic[ID]

    def step(self):
        self.current_step += 1

        # After 10 timesteps, make new ducks
        if self.current_step % 10 == 0:
            self.endseason()

        self.schedule.step()

    def endseason(self):
        for agent in self.schedule.agents:
            if isinstance(agent, FemaleDuckAgent):
                if random.random() < 0.10:
                    maleid = agent.get_id_newduck()
                    agression = self.get_duck_by_id(maleid).agression
                    partner = agent.mate.reset(agression)
                    print ("update to", agression)

        # reset all female ducks for next season.
        for agent in self.schedule.agents:
            if isinstance(agent, FemaleDuckAgent):
                agent.reset()

class DuckAgent(Agent):

    def __init__(self, unique_id, mate_id, model):
        super().__init__(unique_id, model)
        self.mate_id = mate_id

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()

class FemaleDuckAgent(Agent):
    def __init__(self, ID, mate_id,mate, model):
        super().__init__(ID, model)
        self.ID = ID
        self.mate_id = mate_id
        self.mate = mate
        self.numsex = {}
        self.numsex[mate_id] = 100

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True,
            radius=2)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()

    def mating(id):
        # Save the male duck id or make new one in dictionary
        if self.numsex[id]:
            self.numsex[id] += 1
        else:
            self.numsex[id] = 1

    # Create a new generation of ducks
    def get_id_newduck(self):

        duck_id = np.random.choice(list(self.numsex.keys()),
                    p = np.array(list(self.numsex.values()))/sum(self.numsex.values()) )

        return duck_id

    def reset(self):
        self.numsex = {}
        self.numsex[self.mate_id] = 100

class MaleDuckAgent(Agent):
    def __init__(self, ID, mate_id, agression, model):
        super().__init__(ID, model)
        self.ID = ID
        self.mate_id = mate_id
        self.agression = agression

    def move(self):
        mate_pos = self.model.get_duck_by_id(self.mate_id).pos
        self.model.grid.move_agent(self, mate_pos)

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True,
            radius=2)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()

    def reset(self, aggresive):
        self.agression = aggresive

if __name__ == '__main__':
    model = DuckModel(3, 40, 40)
    for time in range(20):
        model.step(time)
