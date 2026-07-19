import random
import click

# Constant for testing - DO NOT use this in your code
TEST_SEED = 20170217


def count_infected(city):
    '''
    Count the number of infected people

    Inputs:
      city (list of strings): the state of all people in the
        simulation at the start of the day
    Returns (int): count of the number of people who are
      currently infected
    '''
    num_infected = 0
    for person in city:
        if person.startswith('I'):
            num_infected += 1
    return num_infected


def has_an_infected_neighbor(city, position):
    '''
    Determine whether a susceptible person at a given position
    has at least one neighbor who is infected.

    Inputs:
      city (list of strings): the state of all people in the
        simulation at the start of the day
      position (int): the position of the person to check
    Returns (bool): True if the person has an infected neighbor,
      False otherwise
    '''
    assert city[position] == "S"

    # Check left neighbor if it exists
    if position > 0:
        if city[position - 1].startswith('I'):
            return True

    # Check right neighbor if it exists
    if position < len(city) - 1:
        if city[position + 1].startswith('I'):
            return True

    return False


def advance_person_at_position(city, position, days_contagious):
    '''
    Advance the disease state of a person from one day to the next.

    Inputs:
      city (list of strings): the state of all people in the
        simulation at the start of the day
      position (int): the position of the person to advance
      days_contagious (int): the number of days a person is contagious
    Returns (string): the new disease state for the person
    '''
    current_state = city[position]

    # If susceptible
    if current_state == 'S':
        if has_an_infected_neighbor(city, position):
            return 'I0'
        else:
            return 'S'

    # If infected
    elif current_state.startswith('I'):
        # Extract the number of days infected
        days_infected = int(current_state[1:])

        # Check if person becomes recovered
        if days_infected >= days_contagious - 1:
            return 'R'
        else:
            return 'I' + str(days_infected + 1)

    # If recovered or vaccinated
    else:  # 'R' or 'V'
        return current_state


def simulate_one_day(city, days_contagious):
    '''
    Model one day in a simulation.

    Inputs:
      city (list of strings): the state of all people in the
        simulation at the start of the day
      days_contagious (int): the number of days a person is contagious
    Returns (list of strings): the state of the city after one day
    '''
    new_city = []
    for i in range(len(city)):
        new_state = advance_person_at_position(city, i, days_contagious)
        new_city.append(new_state)
    return new_city


def vaccinate_city(city, vaccine_effectiveness):
    '''
    Vaccinate susceptible people in the city based on vaccine effectiveness.

    Inputs:
      city (list of strings): the state of all people in the simulation
      vaccine_effectiveness (float): probability that vaccine works
    Returns (list of strings): new city state after vaccination
    '''
    new_city = []
    for person in city:
        if person == 'S':
            # Call random.random() only for susceptible people
            if random.random() < vaccine_effectiveness:
                new_city.append('V')
            else:
                new_city.append('S')
        else:
            new_city.append(person)
    return new_city


def run_simulation(starting_city, days_contagious, random_seed=None, vaccine_effectiveness=0.0):
    '''
    Run the full simulation until no infected people remain.

    Inputs:
      starting_city (list of strings): the initial state of the city
      days_contagious (int): the number of days a person is contagious
      random_seed (int): the seed for the random number generator
      vaccine_effectiveness (float): probability that vaccine works
    Returns (tuple): (final city state, number of days simulated)
    '''
    # Set the random seed if provided
    if random_seed is not None:
        random.seed(random_seed)

    # Vaccinate the city before simulation starts
    city = vaccinate_city(starting_city, vaccine_effectiveness)

    days = 0

    # Continue simulating while there are infected people
    while count_infected(city) > 0:
        city = simulate_one_day(city, days_contagious)
        days += 1

    return (city, days)


def calc_avg_days_to_zero_infections(starting_city, days_contagious, random_seed,
                                     vaccine_effectiveness, num_trials):
    '''
    Calculate the average number of days to reach zero infections.

    Inputs:
      starting_city (list of strings): the initial state of the city
      days_contagious (int): the number of days a person is contagious
      random_seed (int): the starting seed for the random number generator
      vaccine_effectiveness (float): probability that vaccine works
      num_trials (int): number of trials to run
    Returns (float): average number of days to reach zero infections
    '''
    total_days = 0

    for trial in range(num_trials):
        # Increment seed for each trial
        current_seed = random_seed + trial
        city, days = run_simulation(starting_city, days_contagious,
                                    current_seed, vaccine_effectiveness)
        total_days += days

    return total_days / num_trials


@click.command()
@click.argument('city', type=str)
@click.option('--days-contagious', default=2, help='Number of days a person is contagious')
@click.option('--random-seed', default=None, type=int, help='Random seed for simulation')
@click.option('--vaccine-effectiveness', default=0.0, type=float, help='Vaccine effectiveness rate')
@click.option('--num-trials', default=5, type=int, help='Number of trials for average calculation')
@click.option('--task-type', type=click.Choice(['single', 'average']), default='single',
              help='Type of task to run')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def main(city, days_contagious, random_seed, vaccine_effectiveness, num_trials, task_type, debug):
    '''
    Process the command-line arguments and do the work.

    CITY is a comma-separated string representing the initial city state
    (e.g., "S, S, I0")
    '''
    # Parse the city string into a list
    city_list = [state.strip() for state in city.split(',')]

    if debug:
        print(f"Starting city: {city_list}")
        print(f"Days contagious: {days_contagious}")
        print(f"Random seed: {random_seed}")
        print(f"Vaccine effectiveness: {vaccine_effectiveness}")
        print(f"Number of trials: {num_trials}")
        print(f"Task type: {task_type}")
        print()

    if task_type == 'single':
        print("Running one simulation...")
        final_city, days_simulated = run_simulation(
            city_list, days_contagious, random_seed, vaccine_effectiveness
        )
        print(f"Final city: {final_city}")
        print(f"Days simulated: {days_simulated}")

    elif task_type == 'average':
        print("Running multiple trials...")
        avg_days = calc_avg_days_to_zero_infections(
            city_list, days_contagious, random_seed,
            vaccine_effectiveness, num_trials
        )
        print(f"Over {num_trials} trial(s), on average, it took {avg_days} days "
              f"for the number of infections to reach zero")


if __name__ == "__main__":
    main()