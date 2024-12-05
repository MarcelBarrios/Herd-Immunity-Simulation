from virus import Virus
from simulation import Simulation

repro_num = 0.1
mortality_rate = 0.7
virus_name = "test"

vacc_percentage = 0.8
pop_size = 10000
initial_infected = 5

virus = Virus(virus_name, repro_num, mortality_rate)
simulation = Simulation(virus, pop_size, vacc_percentage, initial_infected)

assert simulation.total_infected == 5
assert simulation.pop_size == 10000
assert simulation.total_dead == 0
assert simulation.initial_infected == 5

simulation.run()

assert simulation.pop_size == 10000
assert simulation.total_infected != 10
assert simulation.total_dead != 0
assert simulation.initial_infected == 5

simulation.run()
