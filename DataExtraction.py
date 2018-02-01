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


# save parameters and data of a model
def save_model(duckdata, name):
    pickle.dump( duckdata, open("data/" + name, "wb" ) )

# load parameters and data of a model
def load_model(name):
    return pickle.load( open("data/" + name, "rb" ) )


if __name__ == '__main__':
    n = 500
    width = 100
    height = 100
    season_length = 30
    mutation = 0.1
    partner_egg = 5
    base_succes_mate = 0.1
    runtime = 5000

    # DATA AGGREGATION FROM HERE.....
    from joblib import Parallel, delayed
    from tqdm import tqdm
    # runs the model, saves the data, returns the name of file with the new data
    def run_model():
        m = duckmodel.DuckModel(n,width,height, season_length, mutation, partner_egg, base_succes_mate)

        # run that model
        for _ in range(runtime):
            m.step()

        # save the important values with a datename
        name = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        save_model(DuckData(m), name)
        return name

    duckdatas = []
    n_runs = 2 # number of parralel data aggregations
    n_jobs = 3 # number of cores here
    for _ in tqdm(range(n_runs)):
        duckdatas += Parallel(n_jobs=3)(delayed(run_model)() for _ in range(n_jobs))

    # copy this into duckdatas below to show results
    print(duckdatas)
    # ... TO HERE

    # duckdatas = ['2018-02-01T12:47:15.000001', '2018-02-01T12:46:52.000001', '2018-02-01T12:44:55.000001', '2018-02-01T12:56:12.000001', '2018-02-01T12:58:47.000001', '2018-02-01T12:56:24.000001']
    # all_stds = []
    # end_aggs = []

    # # Two subplots, the axes array is 1-d
    # f, ax = plt.subplots(2, sharex=True)
    # ax[0].set_title("Aggression over time")
    # ax[0].set_ylabel("Mean")
    # ax[1].set_xlabel("Runtime (steps)")
    # ax[1].set_ylabel("Standard deviation")

    # for name in duckdatas:
    #     data = load_model(name)
    #     # save all stds in a single list
    #     all_stds.append(data.stds)

    #     # plot stds and means
    #     ax[0].plot(data.stds)
    #     ax[1].plot(data.means)

    #     # histogram of last aggressions of all runs
    #     # end_aggs = np.concatenate((end_aggs, data.aggs[runtime-1,:]))
    #     # histogram of last aggressions of 1 run
    #     end_aggs = data.aggs[runtime-1,:]

    # plt.show()

    # all_stds = np.array(all_stds)
    # t = range(0,runtime)
    # plt.errorbar(t, np.mean(all_stds, axis=0), yerr=np.var(all_stds, axis=0))
    # plt.show()

    # plt.hist(end_aggs, np.unique(end_aggs), align="mid", rwidth=0.8)
    # plt.show()


    # # these are only some parameter tests
    # for ni in range(0,3):
    #     n = 100 + ni * 300
    #     for sli in range(0,3):
    #         season_length = 5 + 15 * sli
    #         for mi in range(0,3):
    #             mutation = 0.05 + 0.05 * mi
    #             for pei in range(0,4):
    #                 partner_egg = 5 + 10 * pei

    #                 # run the model for these params
    #                 m = duckmodel.DuckModel(n,width,height, season_length, mutation, partner_egg, base_succes_mate)

    #                 # run that model
    #                 for _ in range(runtime):
    #                     m.step()

    #                 # save the important values with a datename
    #                 duckdata = DuckData(m)
    #                 name = datetime.datetime.now().replace(microsecond=0).isoformat()
    #                 print(duckdata.to_string(), '\n')
    #                 save_model(duckdata, name)

    # data = load_model('2018-01-24T05:32:43')
    # print(data.to_string())

    # plt.plot(data.stds)
    # plt.show()
    # plt.plot(data.aggs[:,2])
    # plt.show()
    # plt.plot(data.fsexs[:,2])
    # plt.show()
