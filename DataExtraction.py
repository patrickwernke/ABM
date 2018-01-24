import duckmodel
import numpy as np
import pickle
import datetime
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
        self.stds, self.aggs, self.fsexs = get_data(model)

    # return a string describing this models parameters
    def to_string(self):
        printable = "\n".join([key + ": " + str(value) for (key, value) in self.interesting_vars])
        return "MODEL PARAMETERS:\n" + printable


# Several small functions for extracting the data from the datacollector as np arrays.
def get_data(model):
    assert isinstance(model, duckmodel.DuckModel), "This function takes as input only a DuckModel"
    
    stds = model.datacollector.get_model_vars_dataframe()
    stds = stds.values
    data = model.datacollector.get_agent_vars_dataframe()
    

    
    aggression = data.values[::2]
    size = aggression.shape[0]
    aggression = aggression.reshape((int(size/model.num_agents), model.num_agents))

    female_sex = data.values[1::2]
    female_sex = female_sex.reshape((int(size/model.num_agents), model.num_agents))
    
    return stds, aggression, female_sex
    
def get_standard_deviations(model):
    stds = model.datacollector.get_model_vars_dataframe()
    stds = stds.values
    return stds

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
    n = 100
    width = 100
    height = 100
    season_length = 20
    mutation = 0.1
    partner_egg = 10
    base_succes_mate = 0.2
    runtime = 1500

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

    data = load_model('2018-01-24T05:32:43')
    print(data.to_string())

    plt.plot(data.stds)
    plt.show()
    plt.plot(data.aggs[:,2])
    plt.show()
    plt.plot(data.fsexs[:,2])
    plt.show()
    