from SALib.analyze import sobol
from SALib.sample import saltelli
from SALib.util import read_param_file
from duckmodel import DuckModel
from DataExtraction import get_standard_deviations
from numpy import mean
import numpy as np
from tqdm import tqdm
import pickle
import matplotlib.pyplot as plt
from math import sqrt
from joblib import Parallel, delayed

def run_duck_get_stds(vals, steps, i):
    # set the correct dimensions and ducks for given density
    N = 250
    # width and height are root(density * number_ducks)
    size = int(sqrt(vals[0] * N))

    m = DuckModel(N, size, size, vals[1], vals[2], vals[3], vals[4])
    for _ in range(steps):
        m.step()
    season_length = m.season_length
    std = mean(get_standard_deviations(m)[200:])
    return std

def run_ducks_get_stds(values, steps):
    num_cores = 3
    results = []
    for j in tqdm(range(0, int(values.shape[0]/num_cores))):
        job_num = j * num_cores
        parallel_subresults = Parallel(n_jobs=num_cores)\
                                (delayed(run_duck_get_stds)(values[job_num+i], steps, job_num+i) for i in range(num_cores))
        results += parallel_subresults
    return np.array(results)
    
# get results of our model for number of iterations and write to data/name
def make_results(name):
    problem = read_param_file('./params.txt')
    param_vals = saltelli.sample(problem, 72, calc_second_order=False)
    print("Total amount of iterations:", param_vals.shape[0])
    results = run_ducks_get_stds(param_vals, 5000)
    Si = sobol.analyze(problem, results, calc_second_order=False, conf_level=0.95, print_to_console=True, parallel=True, n_processors=3)
    print(Si)
    pickle.dump( Si, open("data/" + name, "wb" ) )

# get results from data/name file and analyse them
def analyze_results(name):
    Si = pickle.load( open("data/" + name, "rb" ) )

    var_names = ['Density', 'Season length', 'Mutation chance', 'Initial mate copulation', 'Base mating succes']

    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    ax1.errorbar(Si['S1'], var_names, xerr=Si['S1_conf'], fmt='o')
    ax1.plot([0, 0], [-0.3, 4.3], color='darkblue', linestyle='--', lw=2)
    ax1.set_xlabel('Sensitivity')
    ax1.set_title('First order sensitivity')

    ax2.errorbar(Si['ST'], var_names, xerr=Si['ST_conf'], fmt='o')
    ax2.plot([0, 0], [-0.3, 4.3], color='darkblue', linestyle='--', lw=2)
    ax2.set_xlabel('Sensitivity')
    ax2.get_yaxis().set_visible(False)
    ax2.set_title('Total sensitivity')

    plt.show()


if __name__ == '__main__':
    # make_results('naampie')
    analyze_results('Si_std_long')