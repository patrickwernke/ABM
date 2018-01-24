import duckmodel
import numpy as np
import pickle
import dill

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

# save all parameters and data of a model
def save_model(model, name):
    pickle.dump( model.datacollector, open("data/" + name, "wb" ) )

# load all parameters and data of a model
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
    runtime = 20

    m = duckmodel.DuckModel(n,width,height, season_length, mutation, partner_egg, base_succes_mate)

    for _ in range(runtime):
        m.step()
    std, agg, sex = get_data(m)

    save_model(m, "test")
    m2 = load_model("test")

    print(m2.to_string())

    # import matplotlib.pyplot as plt
    # plt.plot(std)
    # plt.show()
    # plt.plot(agg[:,2])
    # plt.show()
    # plt.plot(sex[:,2])
    # plt.show()
    