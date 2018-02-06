import duckmodel
import numpy as np
import pickle
from datetime import datetime
import matplotlib.pyplot as plt


class DuckData():
    def __init__(self, model):
        self.interesting_vars = [
            ('Number of agents',model.num_agents),
            ('Width',model.grid.width),
            ('Height',model.grid.height),
            ('Mutation',model.mutation),
            ('Number of eggs',model.partner_egg),
            ('Base succes mate',model.base_succes_mate),
            ('Season length',model.season_length),
            ('Runtime',model.current_step)
        ]
        self.stds, self.means, self.aggs, self.fsexs = get_data(model)

    # return a string describing this models parameters
    def to_string(self):
        printable = "\n".join([key + ": " + str(value) for (key, value) in self.interesting_vars])
        return "MODEL PARAMETERS:\n" + printable


# Several small functions for extracting the data from the datacollector as np arrays.
def get_data(model):

    stds = get_standard_deviations(model)
    mean = get_mean(model)
    data = model.datacollector.get_agent_vars_dataframe()

    aggression = data.values[::2]
    size = aggression.shape[0]
    aggression = aggression.reshape((int(size/model.num_agents), model.num_agents))

    female_sex = data.values[1::2]
    female_sex = female_sex.reshape((int(size/model.num_agents), model.num_agents))

    return stds, mean, aggression, female_sex

def get_standard_deviations(model):
    model_data = model.datacollector.get_model_vars_dataframe()
    # Standard deviation in first column.
    stds = np.array(model_data.iloc[:,0])
    return stds

def get_mean(model):
    model_data = model.datacollector.get_model_vars_dataframe()
    # Mean in second column.
    mean = np.array(model_data.iloc[:,1])
    return mean

def get_female_sex(model):
    female_sex = data.values[1::2]
    size = female_sex.shape[0]
    female_sex = female_sex.reshape((int(size/model.num_agents), model.num_agents))
    return female_sex

def get_male_aggression(model):
    aggression = data.values[::2]
    size = aggression.shape[0]
    aggression = aggression.reshape((int(size/model.num_agents), model.num_agents))
    return aggression
7
# save parameters and data of a model
def save_model(duckdata, name):
    pickle.dump( duckdata, open("data1/" + name, "wb" ) )

# load parameters and data of a model
def load_model(name):
    return pickle.load( open("data1/" + name, "rb" ) )


if __name__ == '__main__':
    """ Extract a dataframe from the model after each timestep and save it to a file.
    The model output and paramters can later be loaded in again. """
    n = 500
    width = 100
    height = 100
    season_length = 30
    mutation = 0.1
    partner_egg = 8
    base_succes_mate = 0.1
    runtime = 10000

    def run_model():
        """ Run the model once and save model to file. """
        m = duckmodel.DuckModel(n,width,height, season_length, mutation, partner_egg, base_succes_mate)

        # Run that model.
        for _ in range(runtime):
            m.step()

        # Save the important values with a datename.
        name = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        save_model(DuckData(m), name)
        return name

    def data_collection():
        """Collect the data from several runs over multiple cores in parallel. """
        from joblib import Parallel, delayed
        from tqdm import tqdm

        duckdatas = []
        n_runs = 4  # number of parralel data aggregations
        n_jobs = 3 # number of cores here

        for _ in tqdm(range(n_runs)):
            duckdatas += Parallel(n_jobs=3)(delayed(run_model)() for _ in range(n_jobs))

        # copy this into duckdatas below to show results
        print(duckdatas)


    def analyze_results():
        """ Analyze the results of all the model outputs"""
        # The current data files are not present due to their sizes.
        duckdatas = ['2018-02-03T08:15:47.797', '2018-02-03T08:23:58.476', '2018-02-03T08:11:53.388', '2018-02-03T08:53:57.890', '2018-02-03T08:51:21.119', '2018-02-03T08:54:14.803', '2018-02-03T09:33:18.604', '2018-02-03T09:30:22.135', '2018-02-03T09:23:53.713', '2018-02-03T10:01:40.659', '2018-02-03T10:07:57.283', '2018-02-03T10:09:33.320']

        all_stds = []
        all_means = []
        end_aggs = []

        # Two subplots, the axes array is 1-d
        f, ax = plt.subplots(2, sharex=True)
        ax[0].set_title("Aggression over time")
        ax[0].set_ylabel("Standard deviation")
        ax[1].set_xlabel("Runtime (steps)")
        ax[1].set_ylabel("Mean")

        # For every model run load std and mean and plot it.
        for name in duckdatas:
            data = load_model(name)
            # save all stds in a single list
            all_stds.append(data.stds)
            all_means.append(data.means)

            # plot stds and means
            ax[0].plot(data.stds)
            ax[1].plot(data.means)

            # histogram of last aggressions of 1 run
            end_aggs = data.aggs[runtime-1,:]

        plt.show()

        # Average the mean and std and plot with 95% confidence interval.
        all_stds = np.array(all_stds)
        all_means = np.array(all_means)
        t = range(0, runtime)
        plt.subplot(2,1,1)
        plt.plot(t, np.mean(all_stds, axis=0))
        plt.fill_between(t, np.mean(all_stds, axis=0) + np.std(all_stds, axis=0)/len(duckdatas)**0.5, np.mean(all_stds, axis=0) - np.std(all_stds, axis=0)/len(duckdatas)**0.5, alpha = '0.5')
        plt.xlabel("t")
        plt.ylabel("standard deviation")

        plt.subplot(2,1,2)
        plt.plot(t, np.mean(all_means, axis=0))
        plt.fill_between(t, np.mean(all_means, axis=0) + np.std(all_means, axis=0)/len(duckdatas)**0.5, np.mean(all_means, axis=0) - np.std(all_means, axis=0)/len(duckdatas)**0.5, alpha = '0.5')
        plt.xlabel("t")
        plt.ylabel("mean")
        plt.show()

        # show a histogram of the aggression of all the male ducks at the last timestep.
        plt.hist(end_aggs, np.unique(end_aggs), align="left", rwidth=0.8)
        plt.xlabel("level male duck aggressiveness")
        plt.ylabel("number of ducks")
        plt.show()

    analyze_results()
