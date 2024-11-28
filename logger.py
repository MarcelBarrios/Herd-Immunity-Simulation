class Logger(object):
    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = file_name

    # The methods below are just suggestions. You can rearrange these or
    # rewrite them to better suit your code style.
    # What is important is that you log the following information from the simulation:
    # Meta data: This shows the starting situtation including:
    #   population, initial infected, the virus, and the initial vaccinated.
    # Log interactions. At each step there will be a number of interaction
    # You should log:
    #   The number of interactions, the number of new infections that occured
    # You should log the results of each step. This should inlcude:
    #   The population size, the number of living, the number of dead, and the number
    #   of vaccinated people at that step.
    # When the simulation concludes you should log the results of the simulation.
    # This should include:
    #   The population size, the number of living, the number of dead, the number
    #   of vaccinated, and the number of steps to reach the end of the simulation.

    def write_metadata(self, pop_size, initial_infected, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num, date_run):
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        with open(self.file_name, 'w') as file:
            file.write("Simulation Metadata\n")
            file.write(
                "Date Run\tPopulation Size\tInitial Infected\tVaccination Percentage\tVirus Name\tMortality Rate\tBasic Reproduction Number\n")
            file.write(f"""{date_run}\t{pop_size}\t\t\t{initial_infected}\t\t\t\t\t{vacc_percentage}\t\t\t\t\t\t{
                       virus_name}\t{mortality_rate}\t\t\t\t{basic_repro_num}\n""")
            file.write("-----\n")

    def log_interactions(self, current_infected, total_dead, time_step_counter, total_interactions, pop_size, total_vaccinated):
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        with open(self.file_name, 'a') as file:
            file.write(f"Simulation Time Step: {time_step_counter}\n")
            file.write(f"Total Population: {pop_size}\n")
            file.write(f"Currently Infected: {current_infected}\n")
            file.write(f"Total Dead: {total_dead}\n")
            file.write(f"Total Vaccinated: {total_vaccinated}\n")
            file.write(f"Total Interactions: {total_interactions}\n")
            file.write("-----\n")

    def write_final(self, total_living, total_dead, num_vaccinated, reason_ended, total_interactions, vaccinations_from_interactions, deaths_from_interactions):

        with open(self.file_name, 'a') as file:
            file.write("Final Simulation Results\n\n")
            file.write(f"Total Living: {total_living}\n")
            file.write(f"Total Dead: {total_dead}\n")
            file.write(f"Number of Vaccinations: {num_vaccinated}\n")
            file.write(f"Reason Simulation Ended: {reason_ended}\n")
            file.write(f"Total Number of Interactions: {total_interactions}\n")
            file.write(f"""Interactions Resulting in Vaccination: {
                       vaccinations_from_interactions}\n""")
            file.write(f"""Interactions Resulting in Death: {
                       deaths_from_interactions}\n""")

    def answers_log(self, total_interactions, total_dead, total_infected, virus, pop_size, vacc_percentage, vaccine_total_saves):
        log = open("answers.txt", "w")
        log.write(f"""

            What were the inputs you gave the simulation?
            Initial population size: {pop_size}
            Vaccinated percentage: {round(vacc_percentage * 100)}%
            Name of the virus: {virus.name}
            Mortality rate: {virus.mortality_rate}
            Reproductive rate was: {virus.repro_rate}

        """)

        log.write(f"""

            What percentage of the population became infected at some point before the virus burned out?
            {round(total_infected / pop_size * 100)}% of the population became infected at some point before the virus burnt out.

         """)

        log.write(f"""

            What percentage of the population died from the virus?
            {round(pop_size / total_dead)}% of the population died from the virus.

        """)

        log.write(f"""

            Out of all interactions ({total_interactions}) sick individuals had during the entire simulation, how many times, in total, did a vaccination save someone from potentially becoming infected?
            The times a vaccine saved a sick individual was {vaccine_total_saves}.

        """)
