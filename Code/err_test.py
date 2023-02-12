from simul import *

def test_simul() :
    simulation(10, 1, 0, 70, 10, proba=[1, 10, True], save=False)
    simulation(10, 1, 0, 70, 10, proba=[1, 10, False], save=True)
    simulation(10, 1, 0, 70, 10, 1, 120, 2, proba=[1, 10, True], save=False)
    simulation(10, 1, 0, 70, 10, 2, 120, 2, proba=[1, 10, True], save=False)
    simulation(10, 1, 0, 70, 10, 3, 120, 2, proba=[1, 10, True], save=False)
    simulation(10, 1, 0, 70, 10, 4, 120, 2, proba=[1, 10, True], save=False)