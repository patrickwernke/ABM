import random
from numpy import mean, std
import numpy as np
from numpy.random import choice
import matplotlib.pyplot as plt
from tqdm import tqdm

def do_death(N, agents):
    """ Create a new season based on random mutation. """
    death_n = np.random.binomial(N, .5)

    new_genes = [max(min(x + choice([-1,0,1]), 20), 1) for x in choice(list(agents), death_n, True)]
    deaths = choice(range(N), death_n, False)

    for new, old in zip(new_genes, deaths):
        agents[old] = new

    return agents


def run_model(N, iters):
    """ Run the model without spatial elements and aggression."""

    # Create agents.
    agents = []
    for _ in range(N):
        agents.append(random.randint(1,20))

    means= [mean(agents)]
    stds = [std(agents)]

    # Simulate the seasons.
    for _ in tqdm(range(iters)):
        agents = do_death(N, agents)
        means.append(sum(agents)/N)
        stds.append(std(agents))

    plt.subplot(1,2,1)
    plt.xlabel("t(seasons)")
    plt.ylabel("mean")
    plt.plot(means)

    plt.subplot(1,2,2)
    plt.xlabel("t(seasons)")
    plt.ylabel("standard deviation")
    plt.plot(stds)
    plt.show()


if __name__ == '__main__':
    run_model(500, 10000)
