# ABM
This is the project for the Agent-Based Modelling course at the UvA.

Required packages:
DONT USE PIP IN THIS DIRECTORY!
Because the mesa package is already included in these files, a bug in mac and ubuntu (as far as we know), completely breaks your pip! Repairing this issue is a pain, so please just pip install in home directory...
$ pip install SAlib pandas tqdm



DuckModel.py:
Contains the environment(Duckmodel) and the agents(Male/Female DuckAgent).

server.py:
Contains all the information that is needed to run an animation with run_server.py.

run_server.py
Starts an animation of the environment and the ducks on a grid. This animation
loads in the default browser.

DataExtraction.py:
Collect the standard deviation and mean after every season for a given parameter set.
Several runs of the model are run in parallel to account for the stochastic effects.
The result of every simulation run are saved and can be later loaded to give
plots of the std, mean and histogram of the aggressiveness.

main.py:
Calculates the sensitivity analysis for the duckmodel.

test.py:
Test whether all the function give the correct outputs.

moveducks.py:
Give the correct implementation of the Moore and Von Neumann neighborhood.

model_without_ducks.py:
Test without moving duck, to see whether the mutation is the driving force.

Mesa changes:
- Overwritten the Moore and Von Neumann neighborhood.
- Removed the fact that mesa saves the empty spots. After each movement this list
  was updated by removing an element from the list. This causes a lot of new
  unnecessary list creation. For larger grid this speed up the code significantly.
