from utils import (
    setup_game, update_score_text, 
    update_epoch_text, update_highest_score_text
)
from global_vars import GENETIC, Segment

import numpy as np
import random

class DisplayTrainingSimulation:
    pass

class GeneticAlgorithm(DisplayTrainingSimulation):
    def play_game_with_population(self, population):
        """
            population will be used as the weights to
            nerual network
        """
        pass

    def calculate_population_fitness(self, population):
        fitness = []
        for i in range(population.shape[0]):
            fit = self.play_game_with_population(population[i])
            fitness.append(fit)
        return np.array(fitness)

    def select_mating_pool(self, population, fitness):
        parents = np.empty((GENETIC.NUM_PARENT_MATING, population.shape[1]))

        for parent_num in range(GENETIC.NUM_PARENT_MATING):
            max_fitness_idx = np.where(fitness == np.max(fitness))
            max_fitness_idx = max_fitness_idx[0][0]
            parents[parent_num, :] = population[max_fitness_idx, :]
            fitness[max_fitness_idx] = -99999999
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
