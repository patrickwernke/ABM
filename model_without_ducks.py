import random
from numpy import mean, std
import numpy as np
from numpy.random import choice
import matplotlib.pyplot as plt
from tqdm import tqdm

def do_death(N, agents):
    death_n = np.random.binomial(N, .5)
    
    new_genes = [max(min(x + choice([-1,0,1]), 20), 1) for x in choice(list(agents), death_n, True)]
    deaths = choice(range(N), death_n, False)
    
    for new, old in zip(new_genes, deaths):
        agents[old] = new
    
    return agents
    
    
def run_model(N, iters):
    
    agents = []
    for _ in range(N):
        agents.append(random.randint(1,20))
    
    means= [mean(agents)]
    stds = [std(agents)]
    
    for _ in tqdm(range(iters)):
        agents = do_death(N, agents)
        means.append(sum(agents)/N)
        stds.append(std(agents))
    plt.title('Mean over time')
    plt.plot(means)
    plt.show()
    
    plt.title('Std over time')
    plt.plot(stds)
    plt.show()
    
if __name__ == '__main__':
    run_model(500, 10000)