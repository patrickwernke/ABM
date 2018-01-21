from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np
from mesa.datacollection import DataCollector

def std(model):
    x = [x.aggression for x in model.schedule.agents if isinstance(x, MaleDuckAgent)]
    return np.std(x)

class DuckModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height, season_length=20, mutation=0.3, partner_egg=20, base_succes_mate=0.2):
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

            f = FemaleDuckAgent(self.ID, self.ID-1, m, partner_egg, base_succes_mate, self)
            self.duckdic[self.ID] = f
            self.ID += 1

            self.schedule.add(f)
            self.schedule.add(m)

            # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(f, (x, y))
            self.grid.place_agent(m, (x, y))

        # Create a object taht collects the gini coefficient every timestep.
        self.datacollector = DataCollector(
            model_reporters={"Standard deviation of aggression": std},
            agent_reporters={"Data": lambda duck: duck.data}
            )

    def get_male_ducks(self):
        return [duck for duck in self.schedule.agents if isinstance(duck, MaleDuckAgent)]
    
    def get_female_ducks(self):
        return [duck for duck in self.schedule.agents if isinstance(duck, FemaleDuckAgent)]
            
    # Get the duck object given its ID.
    def get_duck_by_id(self, ID):
        return self.duckdic[ID]

    # Make one timestep in the simulation.
    def step(self):
        self.datacollector.collect(self)
        self.current_step += 1

        # After an x amount of timesteps, make a new season
        if self.current_step % self.season_length == 0:
            self.endseason()

        self.schedule.step()

    # Pass on the genes of the ducks that have mated. 50% of all the male ducks die after a season.
    def endseason(self):
        # number of new ducklings
        total_new = np.random.binomial(self.num_agents, .5)

        # get all females in population and get a random sample to kill
        females = self.get_female_ducks()
        kill = random.sample(females, total_new)
        replace = []

        # get random females staged for reproduction
        for i in range(0, total_new):
            # the female and male that reproduce (randomly chosen from all population)
            mother = random.choice(females)
            # the male that reproduces (randomly chosen from the mother's encounters)
            father = self.get_duck_by_id(mother.get_id_newduck())
            # save the male's traits
            child_traits = (father.aggression,)
            replace.append(child_traits)

        # replace the male mates in the kill list with new ones
        for i in range(len(kill)):
            female = kill[i]
            mate_traits = replace[i]
            # set the new mates traits
            female.mate.reset(mate_traits)
            # reset the females sexual encounters
            female.reset()

class FemaleDuckAgent(Agent):
    def __init__(self, ID, mate_id,mate, partner_egg, base_succes_mate, model):
        super().__init__(ID, model)
        self.ID = ID
        self.mate_id = mate_id
        self.mate = mate
        self.numsex = {}
        self.partner_egg = partner_egg
        self.numsex[mate_id] = partner_egg
        self.base_succes = base_succes_mate
        
        # because mesa does not actually work
        self.data = partner_egg

    # Move the female duck into a random position within a maximum radius.
    def step(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False,
            radius=2)

        # Loop over every possible cell until a cell with no female has been found.
        # If no cell is found, stay at current cell
        while possible_steps:
            new_position = random.choice(possible_steps)

            # Content contains other females if they are on the new spot.
            content = self.model.grid.iter_cell_list_contents(new_position)
            content = [x for x in content if isinstance(x, FemaleDuckAgent)]

            if not content:
                self.model.grid.move_agent(self, new_position)
                break

            possible_steps.remove(new_position)

    # Calculate the chance of a succesfull mating.
    def succes_mating(self):
        max_distance = 20

        # Succes chance linearly increases if the male is further away until some threshold.
        distance_ownmale = np.linalg.norm(np.array(self.mate.pos) - np.array(self.pos))
        variable_chance = (1 - self.base_succes) * (min(1, distance_ownmale / max_distance))

        return self.base_succes + variable_chance

    # Add one mating to the possible list of mates.
    def mating(self,ID):
        if np.random.random() < self.succes_mating():
            self.numsex[ID] = self.numsex.get(ID, 0) + 1
            # represents number of succesful sexual encounters
            self.data+=1

    # choose a male from all sexual encounters in this season
    def get_id_newduck(self):
        # get a random duck from sexytimes
        duck_id = np.random.choice(list(self.numsex.keys()),
                    p = np.array(list(self.numsex.values()))/sum(self.numsex.values()) )

        return duck_id

    # Reset the mate list of the duck.
    def reset(self):
        self.numsex = {}
        self.numsex[self.mate_id] = self.partner_egg
        self.data = self.partner_egg

class MaleDuckAgent(Agent):
    def __init__(self, ID, mate_id, aggression, mutation, model):
        super().__init__(ID, model)
        self.ID = ID
        self.mate_id = mate_id
        self.aggression = aggression
        self.mutation = mutation
        
        # data gathering
        self.data=aggression

    # Make a step towards the female and mate if they are in range.
    def step(self):
        random_number = abs(int(np.random.normal(0, self.aggression)))
        mate_pos = self.model.get_duck_by_id(self.mate_id).pos
        neighbors = self.model.grid.get_neighbors(mate_pos, moore=False, include_center=False, radius=random_number)
        neighbors = [duck for duck in neighbors if isinstance(duck, FemaleDuckAgent)]

        if neighbors:
            victim = np.random.choice(neighbors)
            next_position = victim.pos
            self.model.grid.move_agent(self, next_position)
            victim.mating(self.ID)
        else:
            possible_steps = self.model.grid.get_neighborhood(
                mate_pos,
                moore=False,
                include_center=True,
                radius=random_number)
            next_position = random.choice(possible_steps)
            self.model.grid.move_agent(self, next_position)

    # Reset the traits of the duck and add a mutation.
    def reset(self, traits):
        # traits only consist of aggression
        aggression = traits[0]
        if np.random.random() < self.mutation:
            self.aggression = aggression + np.random.choice([-1,1])
        else:
            self.aggression = aggression

        self.aggression = max(self.aggression, 1)
        self.aggression = min(self.aggression, 20)
        # data gathering
        self.data = self.aggression

if __name__ == '__main__':
    model = DuckModel(3, 40, 40)
    for time in range(20):
        model.step()
