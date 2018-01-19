# model.py
from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np
from mesa.datacollection import DataCollector

def gini_aggression(model):
    x = sorted([x.aggression for x in model.schedule.agents if isinstance(x, MaleDuckAgent)])
    N = len(x)
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B)


class DuckModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height, season_length, mutation, partner_egg):
        self.running=True
        self.ID = 0
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.current_step = 0
        self.season_length = season_length

        self.duckdic={}

        # Create agents
        for _ in range(self.num_agents):
            m = MaleDuckAgent(self.ID, self.ID+1, 5, mutation, self)
            self.duckdic[self.ID] = m
            self.ID += 1

            f = FemaleDuckAgent(self.ID, self.ID-1, m, partner_egg, self)
            self.duckdic[self.ID] = f
            self.ID += 1

            self.schedule.add(f)
            self.schedule.add(m)

            # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(f, (x, y))
            self.grid.place_agent(m, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"aggression": gini_aggression}
            )

    def get_duck_by_id(self, ID):
        return self.duckdic[ID]

    def step(self):
        self.datacollector.collect(self)
        self.current_step += 1

        # After 10 timesteps, make new ducks
        if self.current_step % self.season_length == 0:
            self.endseason()

        self.schedule.step()

    def endseason(self):
        for agent in self.schedule.agents:
            if isinstance(agent, FemaleDuckAgent):
                if random.random() < 0.50:
                    maleid = agent.get_id_newduck()
                    aggression = self.get_duck_by_id(maleid).aggression
                    partner = agent.mate.reset(aggression)
                    #print ("update to", aggression)

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
    def __init__(self, ID, mate_id,mate, partner_egg, model):
        super().__init__(ID, model)
        self.ID = ID
        self.mate_id = mate_id
        self.mate = mate
        self.numsex = {}
        self.partner_egg = partner_egg
        self.numsex[mate_id] = partner_egg

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=2)

        # Loop over every possible cell until an empty one has been found

        while possible_steps:
            new_position = random.choice(possible_steps)

            # Content returns a list of objects
            content = self.model.grid.iter_cell_list_contents(new_position)
            content = [x for x in content if isinstance(x, FemaleDuckAgent)]

            if not content:
                self.model.grid.move_agent(self, new_position)
                break

            possible_steps.remove(new_position)


    def step(self):
        self.move()

    def succes_mating(self):
        base_chance = 0.25
        max_distance = 20

        # Succes chance linearly increases if the male is further away until some threshold
        distance_ownmale = np.linalg.norm(np.array(self.mate.pos) - np.array(self.pos))
        variable_chance = (1 - base_chance) * (min(1, distance_ownmale / max_distance))

        return base_chance + variable_chance


    def mating(self,ID):
        if np.random.random() < self.succes_mating():
            self.numsex[ID] = self.numsex.get(ID, 0) + 1

    # Create a new generation of ducks
    def get_id_newduck(self):
        duck_id = np.random.choice(list(self.numsex.keys()),
                    p = np.array(list(self.numsex.values()))/sum(self.numsex.values()) )

        return duck_id

    def reset(self):
        self.numsex = {}
        self.numsex[self.mate_id] = self.partner_egg

class MaleDuckAgent(Agent):
    def __init__(self, ID, mate_id, aggression, mutation, model):
        super().__init__(ID, model)
        self.ID = ID
        self.mate_id = mate_id
        self.aggression = aggression
        self.mutation = mutation

    def move(self):
        random_number = abs(int(np.random.normal(0, self.aggression)))
        mate_pos = self.model.get_duck_by_id(self.mate_id).pos
        neighbors = self.model.grid.get_neighbors(mate_pos, True, include_center=False, radius=random_number)
        neighbors = [duck for duck in neighbors if isinstance(duck, FemaleDuckAgent)]

        if neighbors:
            victem = np.random.choice(neighbors)
            next_position = victem.pos
            self.model.grid.move_agent(self, next_position)
            victem.mating(self.ID)
        else:
            possible_steps = self.model.grid.get_neighborhood(
                mate_pos,
                moore=True,
                include_center=True,
                radius=random_number)
            next_position = random.choice(possible_steps)
            self.model.grid.move_agent(self, next_position)

    def step(self):
        self.move()

    def reset(self, aggressive):
        if np.random.random() < self.mutation:
            self.aggression = aggressive + np.random.choice([-1,1])
        else:
            self.aggression = aggressive
        self.aggression = max(self.aggression, 1)
        self.aggression = min(self.aggression, 20)

if __name__ == '__main__':
    model = DuckModel(3, 40, 40)
    for time in range(20):
        model.step(time)
