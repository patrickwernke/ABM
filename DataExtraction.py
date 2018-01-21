import duckmodel
import numpy as np

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
    
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    m = duckmodel.DuckModel(20,30,30)
    for _ in range(200):
        m.step()
    std, agg, sex = get_data(m)
    for a in agg:
        print(a)
    plt.plot(std)
    plt.show()
    plt.plot(agg[:,2])
    plt.show()
    plt.plot(sex[:,2])
    plt.show()
    