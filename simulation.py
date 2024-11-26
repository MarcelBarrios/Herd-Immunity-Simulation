from virus import Virus
from logger import Logger
from person import Person
import random
import sys
random.seed(42)


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        self.logger = Logger("result.txt")
        # TODO: Store the virus in an attribute
        self.virus = virus
        # TODO: Store pop_size in an attribute
        self.pop_size = int(pop_size)
        # TODO: Store the vacc_percentage in a variable
        self.vacc_percentage = float(vacc_percentage)
        # TODO: Store initial_infected in a variable
        self.initial_infected = int(initial_infected)
        # You need to store a list of people (Person instances)
        # Some of these people will be infected some will not.
        # Use the _create_population() method to create the list and
        # return it storing it in an attribute here.
        # TODO: Call self._create_population() and pass in the correct parameters.
        self.population = self._create_population()
        self.newly_infected = []
        self.current_infected = 0
        self.total_infected = 0
        self.total_vaccinated = 0
        self.total_dead = 0

    def _create_population(self):
        # TODO: Create a list of people (Person instances). This list
        # should have a total number of people equal to the pop_size.
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        people_list = []
        infected_count = 0
        for person_id in range(self.pop_size):
            if infected_count < self.initial_infected:
                person = Person(person_id, is_vaccinated=False,
                                infection=self.virus)
                infected_count += 1
            else:
                is_vaccinated = random.random() < self.vacc_percentage
                person = Person(
                    person_id, is_vaccinated=is_vaccinated, infection=None)

            people_list.append(person)

        # TODO: Return the list of people
        return people_list

    def _simulation_should_continue(self):
        # This method will return a booleanb indicating if the simulation
        # should continue.
        # The simulation should not continue if all of the people are dead,
        # or if all of the living people have been vaccinated.
        # TODO: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.
        living_people = []

        for person in self.population:
            if person.is_alive:
                living_people.append(person)

        if len(living_people) == 0:
            return False

        all_vaccinated = True
        for person in living_people:
            if not person.is_vaccinated:
                all_vaccinated = False
                break

        if all_vaccinated:
            return False

        # simulation keeps going
        return True

    def run(self):
        # This method starts the simulation. It should track the number of
        # steps the simulation has run and check if the simulation should
        # continue at the end of each step.

        self.time_step_counter = 0
        should_continue = True

        # TODO: Write meta data to the logger. This should be starting
        # statistics for the simulation. It should include the initial
        # population size and the virus.
        self.logger.write_metadata(
            pop_size=self.pop_size,
            initial_infected=self.initial_infected,
            vacc_percentage=self.vacc_percentage,
            virus_name=self.virus.name,
            mortality_rate=self.virus.mortality_rate,
            basic_repro_num=self.virus.repro_rate,
        )

        while should_continue:
            # TODO: Increment the time_step_counter
            time_step_counter += 1
            # TODO: for every iteration of this loop, call self.time_step()
            # Call the _simulation_should_continue method to determine if
            # the simulation should continue
            should_continue = self._simulation_should_continue()
            self.time_step()

        # TODO: When the simulation completes you should conclude this with
        # the logger. Send the final data to the logger.
        self.logger.write_final(
            total_living=self.pop_size,
            total_dead=self.total_dead,
            num_vaccinated=num_vaccinated,
            reason_ended=reason_ended,
            total_interactions=total_interactions,
            vaccinations_from_interactions=vaccinations_from_interactions,
            deaths_from_interactions=deaths_from_interactions,
        )

    def time_step(self):
        # This method will simulate interactions between people, calulate
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other
        # people in the population
        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person

        for person in self.population:
            if person.infection and person.is_alive:
                interactions = 0
                while interactions < 100:
                    random_person = random.choice(self.population)
                    while not random_person.is_alive and not random_person.is_vaccinated:
                        random_person = random.choice(self.population)
                    self.interaction(person, random_person)
                    interactions += 1

                if person.did_survive_infection() == True:
                    self.current_infected -= 1
                    person.is_vaccinated = True
                    self.total_vaccinated += 1

                else:
                    person.is_alive = False
                    self.total_dead += 1
                    self.current_infected -= 1

        self._infect_newly_infected()

    def interaction(self, infected_person, random_person):
        # TODO: Finish this method.
        # The possible cases you'll need to cover are listed below:
        # random_person is vaccinated:
        #     nothing happens to random person.
        # random_person is already infected:
        #     nothing happens to random person.
        # random_person is healthy, but unvaccinated:
        #     generate a random number between 0.0 and 1.0.  If that number is smaller
        #     than repro_rate, add that person to the newly infected array
        #     Simulation object's newly_infected array, so that their infected
        #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.
        if random_person.is_vaccinated:
            pass
        elif random_person.infection:
            pass
        else:
            if random.random() < self.virus.repro_rate:
                self.newly_infected.append(random_person)

    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.newly_infected:
            person.infection = self.virus
            self.total_infected += 1
            self.current_infected += 1
            self.population.append(person)

        self.newly_infected = []


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the imulation
    virus = Virus(virus, pop_size, vacc_percentage, initial_infected)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()
