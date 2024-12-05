import os
from logger import Logger
from virus import Virus


def test_logger_files():
    result_file = "result_test.txt"

    logger = Logger(result_file)

    logger.write_metadata(
        pop_size=1000,
        initial_infected=10,
        vacc_percentage=0.8,
        virus_name="TestVirus",
        mortality_rate=0.5,
        basic_repro_num=0.3,
        date_run="2024-11-24"
    )

    logger.log_interactions(
        current_infected=50,
        total_dead=5,
        time_step_counter=1,
        total_interactions=200,
        pop_size=1000,
        total_vaccinated=700
    )

    logger.write_final(
        total_living=950,
        total_dead=50,
        num_vaccinated=800,
        reason_ended="All infected individuals recovered.",
        total_interactions=200,
        vaccinations_from_interactions=100,
        deaths_from_interactions=10
    )

    repro_num = 0.1
    mortality_rate = 0.7
    virus_name = "test"

    virus = Virus(virus_name, repro_num, mortality_rate)

    logger.answers_log(
        total_interactions=200,
        total_dead=50,
        total_infected=100,
        virus=virus,
        pop_size=1000,
        vacc_percentage=0.8,
        vaccine_total_saves=50
    )

    assert os.path.exists(result_file), "Result file not created."
    with open(result_file, 'r') as file:
        content = file.read()
        assert len(content) > 0, "Result file is empty."

    assert os.path.exists("answers.txt"), "Answers file not created."
    with open("answers.txt", 'r') as file:
        content = file.read()
        assert len(content) > 0, "Answers file is empty."
