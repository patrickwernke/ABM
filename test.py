import DataExtraction
import duckmodel
import moveducks
from copy import deepcopy

def test_moveducks():
    model = duckmodel.DuckModel(1, 2, 2)
    radius1 = moveducks.von_neumann_neighborhood(model, (1,1), 1)
    assert len(list(radius1)) == 5, 'Failed test 1, von neumann neighborhood'
    
    ducks = moveducks.get_neighbors(model, radius1)
    assert len(ducks) == 2 or len(ducks) == 0, 'Failed test 2, getting neighbors'
    
    radius5 = moveducks.von_neumann_neighborhood(model, (1,1), 5)
    ducks = moveducks.get_neighbors(model, radius5)
    assert len(ducks) == 2, 'Failed test 3, getting neighbors'

    
def test_duckmodel():
    model = duckmodel.DuckModel(10, 6, 6, mutation=0.5, season_length=5)
    assert duckmodel.std(model) >= 0, 'Failed test 4, standard deviation'
    assert 20 >= duckmodel.mean(model) >= 0, 'Failed test 5, mean'
    
    for duck in model.get_male_ducks():
        assert isinstance(duck, duckmodel.MaleDuckAgent), 'Failed test 6, male ducks'
            
    for duck in model.get_female_ducks():
        assert isinstance(duck, duckmodel.FemaleDuckAgent), 'Failed test 7, female ducks'   

    assert len(model.get_male_ducks()) == len(model.get_female_ducks()), 'Failed test 8, number of ducks'
    
    for i in range(20):
        assert isinstance(model.get_duck_by_id(i), duckmodel.MaleDuckAgent) or\
            isinstance(model.get_duck_by_id(i), duckmodel.FemaleDuckAgent), 'Failed test 9, duck by ID'
    
    means = []
    stds = []
    for i in range(100):
        model.step()
        means.append(duckmodel.mean(model))
        stds.append(duckmodel.std(model))
    assert model.current_step == 100, 'Failed test 10, step counter'
    assert means.count(means[0]) != len(means), 'Failed test 11, step means (very small chance of failing randomly)'
    assert stds.count(stds[0]) != len(stds), 'Failed test 12, step stds (very small chance of failing randomly)'
    
    means = []
    stds = []
    for _ in range(20):
        model.endseason()
        means.append(duckmodel.mean(model))
        stds.append(duckmodel.std(model))
    assert model.current_step == 100, 'Failed test 13, step counter after endseason'
    assert means.count(means[0]) != len(means), 'Failed test 14, step means after endseason (very small chance of failing randomly)'
    assert stds.count(stds[0]) != len(stds), 'Failed test 15, step stds endseason (very small chance of failing randomly)'
    
def test_ducks():
    model = duckmodel.DuckModel(10, 6, 6, mutation=1, season_length=500000, partner_egg=10)
    fduck = model.get_female_ducks()[0]
    mduck = model.get_male_ducks()[1]
    fpos = []
    mpos = []
    sexdic = deepcopy(fduck.numsex)
    assert sexdic.pop(fduck.mate_id) == 10, 'Failed test 16, partner mating'
    assert not sexdic, 'Failed test 17, mating dict'
    
    for _ in range(30):
        model.step()
        fpos.append(fduck.pos)
        mpos.append(fduck.pos)
    assert fpos.count(fpos[0]) != len(fpos), 'Failed test 18, female movement (very small chance of failing randomly)'
    assert mpos.count(mpos[0]) != len(mpos), 'Failed test 19, male movement (very small chance of failing randomly)'
    
    sexdic = deepcopy(fduck.numsex)
    assert sexdic.pop(fduck.mate_id) == 10, 'Failed test 20, partner mating'
    assert sexdic, 'Failed test 21, mating dict'

    aggs = []
    for _ in range(100):
        model.endseason()
        sexdic = deepcopy(fduck.numsex)
        assert sexdic.pop(fduck.mate_id) == 10, 'Failed test 22, partner mating'
        assert not sexdic, 'Failed test 23, mating dict'
        aggs.append(mduck.aggression)
    assert aggs.count(aggs[0]) != len(aggs), 'Failed test 24, mutation (very small chance of failing randomly)'
    
    for _ in range(100):
        mduck.reset((3,))
        assert mduck.aggression == 2 or mduck.aggression == 4, 'Failed test 25, mutation'
    
if __name__ == "__main__":
    test_moveducks()
    test_duckmodel()
    test_ducks()
    