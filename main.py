from SALib.analyze import sobol
from SALib.sample import saltelli
from SALib.util import read_param_file
from duckmodel import DuckModel
from DataExtraction import get_standard_deviations
from numpy import mean
import numpy as np
from tqdm import tqdm
import pickle

def run_duck_get_stds(values, steps):
    result = np.zeros(values.shape[0])
    for i, vals in tqdm(enumerate(values)):        
        m = DuckModel(vals[0], 60, 60, vals[1], vals[2], vals[3], vals[4])
        for _ in range(steps):
            m.step()
        season_length = m.season_length
        std = mean(get_standard_deviations(m)[200:])
        result[i] = std
    return result
    
# get results of our model for number of iterations and write to data/name
def make_results(name):
    problem = read_param_file('./params.txt')
    param_vals = saltelli.sample(problem, 90, calc_second_order=True)
    print("Total amount of iterations:", param_vals.shape[0])
    results = run_duck_get_stds(param_vals, 1200)
    Si = sobol.analyze(problem, results, calc_second_order=True, conf_level=0.95, print_to_console=True)
    print(Si)
    pickle.dump( Si, open("data/" + name, "wb" ) )

# get results from data/name file and analyse them
def analyze_results(name):
    Si = pickle.load( open("data/" + name, "rb" ) )
    print(Si)
    # TODO analysis


if __name__ == '__main__':
    # make_results('naampje_voor_bestandje')
    analyze_results('Si_aggMating_1080it')