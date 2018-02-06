def von_neumann_neighborhood(model, pos, radius):
    """
    Given a position and a radius in a model,
    returns the correct von neumann neighborhood.

    If radius is large compared to the grid, can
    return certain positions more than once.

    Mesa's implementation is entirely incorrect,
    thus necessitating this function.
    """


    max_height = model.grid.height
    max_width = model.grid.width

    p = []

    #i=j=0
    p.append(pos)
    #i=0
    for j in range(1, radius + 1):
        p.append(( (pos[0]) % max_width, (pos[1] + j) % max_height))
        p.append(( (pos[0]) % max_width, (pos[1] - j) % max_height))

    for i in range(1, radius+1):
        #j=0
        p.append(( (pos[0] + i) % max_width, (pos[1]) % max_height))
        p.append(( (pos[0] - i) % max_width, (pos[1]) % max_height))
        for j in range(1, radius + 1 - i):
            p1 = ( (pos[0] + i) % max_width, (pos[1] + j) % max_height)
            p2 = ( (pos[0] + i) % max_width, (pos[1] - j) % max_height)
            p3 = ( (pos[0] - i) % max_width, (pos[1] + j) % max_height)
            p4 = ( (pos[0] - i) % max_width, (pos[1] - j) % max_height)
            for po in [p1,p2,p3,p4]:
                p.append(po)
    return p

def get_neighbors(model, neighborhood):
    """Returns all agents in a neighborhood"""
    agents = model.grid.get_cell_list_contents(neighborhood)
    return list(set(agents))

if __name__ == '__main__':
    pass
