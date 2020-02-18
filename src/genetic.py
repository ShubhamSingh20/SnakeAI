from utils import (
    setup_game, update_score_text, 
    update_epoch_text, update_highest_score_text
)
from neural_network import forward_propagation
from global_vars import GENETIC, Segment
from snake import Snake
import numpy as np
import random

class DisplayTrainingSimulation:
    def __init__(self):
        super().__init__()

class GeneticAlgorithm(DisplayTrainingSimulation):
    def play_game_with_population(self, epoch, population):
        """
            population will be used as the weights to the
            nerual network
        """
        for _ in range(GENETIC.TESTS_PER_GAME):
            # Number of games to playper population
            # snake intialization goes here.
            snake = Snake()
            x_change, y_change = Segment.DIFF, 0
            count_same_direction, reward = 0, 0
            snake.create_fruit()
            snake.intial_movement()
            snake_is_alive = True

            for _ in range(GENETIC.STEPS_PER_GAME):
                # Maximum numbers of moves which are allowed to be made 
                # or just die, most of the time snake will die before hitting
                # this limit.

                current_direction_vector, is_front_blocked, \
                    is_left_blocked, is_right_blocked = snake.blocked_directions_vector()

                angle, snake_direction_vector, apple_direction_vector_normalized,\
                    snake_direction_vector_normalized = snake.get_angle_to_fruit()
                
                predictions = []

                def get_direction_prediction():
                    direction = np.argmax(np.array(forward_propagation(np.array([
                        is_left_blocked, is_front_blocked, is_right_blocked, 
                        apple_direction_vector_normalized[0], snake_direction_vector_normalized[0],
                        apple_direction_vector_normalized[1], snake_direction_vector_normalized[1]
                    ]).reshape(-1, 7), population))) - 1

                    if direction == 0:
                        return 'left'

                    if direction == 2: 
                        return snake.direction

                    if direction == 2:
                        return 'right'
                    

                predicted_direction = get_direction_prediction()

                if predicted_direction == snake.direction:
                    count_same_direction += 1
                else:
                    count_same_direction = 0
                    snake.move(predicted_direction)
                
                if not snake.is_alive():
                    reward += -150
                    break

                reward += 0


            del snake.allspriteslist, snake.fruit, snake

    def calculate_population_fitness(self, population):
        fitness = []
        for i in range(population.shape[0]):
            fit = self.play_game_with_population(1+i, population[i])
            fitness.append(fit)
        return np.array(fitness)

    def select_mating_pool(self, population, fitness):
        parents = np.empty((GENETIC.NUM_PARENT_MATING, population.shape[1]))

        for parent_num in range(GENETIC.NUM_PARENT_MATING):
            max_fitness_idx = np.where(fitness == np.max(fitness))
            max_fitness_idx = max_fitness_idx[0][0]
            parents[parent_num, :] = population[max_fitness_idx, :]
            fitness[max_fitness_idx] = -10**8
        return parents
    
    def generation_crossover(self, parents, offspring_size):
        offspring = np.empty(offspring_size)

        for k in range(offspring_size[0]): 
            while True:
                parent1_idx = random.randint(0, parents.shape[0] - 1)
                parent2_idx = random.randint(0, parents.shape[0] - 1)
                # produce offspring from two parents if they are different
                if parent1_idx != parent2_idx:
                    for j in range(offspring_size[1]):
                        if random.uniform(0, 1) < 0.5:
                            offspring[k, j] = parents[parent1_idx, j]
                        else:
                            offspring[k, j] = parents[parent2_idx, j]
                    break
        return offspring

    def offspring_mutation(self, offspring_crossover):
        """
        Adding some variations to the offsrping using mutation.
        """
        for idx in range(offspring_crossover.shape[0]):
            for _ in range(25):
                i = random.randint(0,offspring_crossover.shape[1]-1)

            random_value = np.random.choice(
                np.arange(-1,1,step=0.001), size=(1), replace=False
            )
            offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value

        return offspring_crossover


class TrainSnake(GeneticAlgorithm):
    def __init__(self, **kwargs):
        self.new_population = kwargs.get(
            'population', np.random.choice(
                np.arange(-1,1,step=0.01), replace=True,
                size=GENETIC.POPULATION_SIZE,
            )
        )

    def training_generation(self):
        for generation in range(GENETIC.NUM_GEN):
            fitness = self.calculate_population_fitness(self.new_population)
            parents = self.select_mating_pool(self.new_population, fitness)
            offspring_crossover = self.generation_crossover(
                parents, (GENETIC.SOL_PER_POP - parents.shape[0], GENETIC.NUM_WEIGHTS)
            )
            offspring_mutation = self.offspring_mutation(offspring_crossover)
            self.new_population[0:parents.shape[0], :] = parents
            self.new_population[parents.shape[0]:, :] = offspring_mutation
