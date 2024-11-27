from datetime import datetime
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
        self.num_vaccinated = 0
        self.current_infected = 0
        self.total_infected = 0
        self.population = self._create_population()
        self.newly_infected = []
        self.total_interactions = 0
        self.vaccine_total_saves = 0
        self.total_vaccinated = 0
        self.total_dead = 0
        self.deaths_from_interactions = 0

    def _create_population(self):
        # TODO: Create a list of people (Person instances). This list
        # should have a total number of people equal to the pop_size.
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        people_list = []

        poplulation_vaccinated = int(self.vacc_percentage * self.pop_size)
        self.current_vaccinated = poplulation_vaccinated

        population_unvaccinated = self.pop_size - \
            poplulation_vaccinated - self.initial_infected

        id = 0

        for i in range(poplulation_vaccinated):
            id += 1
            self.num_vaccinated += 1
            person = Person(id, True, None)
            people_list.append(person)

        for i in range(population_unvaccinated):
            id += 1
            person = Person(id, False, None)
            people_list.append(person)

        for i in range(self.initial_infected):
            id += 1
            self.current_infected += 1
            self.total_infected += 1
            person = Person(id, False, self.virus)
            people_list.append(person)

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

        simulation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            date_run=simulation_date
        )

        while should_continue:
            # TODO: Increment the time_step_counter
            self.time_step_counter += 1
            # TODO: for every iteration of this loop, call self.time_step()
            # Call the _simulation_should_continue method to determine if
            # the simulation should continue
            should_continue = self._simulation_should_continue()
            self.time_step()

            self.logger.log_interactions(
                self.current_infected,
                self.total_dead,
                self.time_step_counter,
                self.total_interactions,
                self.pop_size,
                self.total_vaccinated
            )

        self.logger.answers_log(
            self.total_interactions,
            self.total_dead,
            self.total_infected,
            self.virus,
            self.pop_size,
            self.vacc_percentage,
            self.vaccine_total_saves
        )

        living_people = []

        for person in self.population:
            if person.is_alive:
                living_people.append(person)

        if len(living_people) == 0:
            reason_ended = "All people are dead."

        else:
            all_vaccinated = True

            for person in living_people:
                if not person.is_vaccinated:
                    all_vaccinated = False
                    break

            if all_vaccinated:
                reason_ended = "All living people are vaccinated."

        # TODO: When the simulation completes you should conclude this with
        # the logger. Send the final data to the logger.
        self.logger.write_final(
            total_living=self.pop_size,
            total_dead=self.total_dead,
            num_vaccinated=self.num_vaccinated,
            reason_ended=reason_ended,
            total_interactions=self.total_interactions,
            vaccinations_from_interactions=self.total_vaccinated,
            deaths_from_interactions=self.deaths_from_interactions,
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
                    self.deaths_from_interactions += 1
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
        self.total_interactions += 1

        if random_person.is_vaccinated:
            self.vaccine_total_saves += 1
        elif random_person.is_alive == True and random_person.is_vaccinated == False and random_person.infection == None:
            if random.random() < self.virus.repro_rate:
                self.newly_infected.append(random_person)
                self.population.remove(random_person)

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
    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()
