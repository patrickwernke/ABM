import DataExtraction
import duckmodel
import moveducks


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
    model = duckmodel.DuckModel(10,6,6)
    assert duckmodel.std(model) >= 0, 'Failed test 4, standard deviation'
    assert 20 >= duckmodel.mean(model) >= 0, 'Failed test 5, mean'
    
    for duck in model.get_male_ducks():
        assert isinstance(duck, duckmodel.MaleDuckAgent), 'Failed test 6, male ducks'
            
    for duck in model.get_female_ducks():
        assert isinstance(duck, duckmodel.FemaleDuckAgent), 'Failed test 7, female ducks'    
    
    for i in range(20):
        assert isinstance(model.get_duck_by_id(i), duckmodel.MaleDuckAgent) or\
            isinstance(model.get_duck_by_id(i), duckmodel.FemaleDuckAgent), 'Failed test 8, duck by ID'
            
    for _ in range(100):
        model.step()
    assert model.current_step == 100, 'Failed test 9, step'
    
    
    
    
def test_dataextraction():
    raise NotImplementedError    

if __name__ == "__main__":
    test_moveducks()
    test_duckmodel()
    test_dataextraction()
