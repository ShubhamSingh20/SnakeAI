from neural_network import forward_propagation
from utils import (
    setup_game, update_score_text, 
    update_epoch_text, update_highest_score_text
)
from global_vars import (
    GENETIC, Segment, Color
)
from snake import Snake
import numpy as np
import pygame
import random
import time


class DisplayTrainingSimulation:
    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.screen, self.myfont = setup_game()
        self.start_ticks = pygame.time.get_ticks()
    
    def display_snake(self, snake, epoch, highest_score):
        def __init__(self):
            super().__init__()

        if snake.ate_fruit():
            snake.give_point(change_fruit=True)
            snake.insert_new_segment()
        
        self.screen.fill(Color.BLACK)
        snake.draw(self.screen)

        update_score_text(
            self.screen, self.myfont, "Score: {0}".format(snake.score)
        )
        update_highest_score_text(
            self.screen, self.myfont,
            "Highest Score: {0}".format(highest_score)
        )

        run_time = (pygame.time.get_ticks()-self.start_ticks) / 1000
        run_time = time.strftime("%M min:%S sec", time.gmtime(run_time)) 

        update_epoch_text(
            self.screen, self.myfont,
            "Training Epoch: {0} ({1})".format(epoch,  run_time)
        )

        pygame.display.flip()
        self.clock.tick(20) # Framerate
    
    def kill_simulation(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


class GeneticAlgorithm(DisplayTrainingSimulation):
    def play_game_with_population(self, epoch, population):
        """
            population will be used as the weights to the
            nerual network
        """
        reward_score, score, max_score = 0, 0, 0
        for _ in range(GENETIC.TESTS_PER_GAME):
            # Number of games to playper population
            # snake intialization goes here.
            snake = Snake()
            count_same_direction = 0
            snake.create_fruit()
            snake.intial_movement()

            for _ in range(GENETIC.STEPS_PER_GAME):
                # Maximum numbers of moves which are allowed to be made 
                # or just die, most of the time snake will die before hitting
                # this limit.

                self.kill_simulation()
                is_front_blocked, is_left_blocked, \
                    is_right_blocked = snake.blocked_directions_vector()

                angle, snake_direction_vector, fruit_direction_vector_normalized,\
                    snake_direction_vector_normalized = snake.get_angle_with_fruit()
                
                predictions = []

                def get_direction_prediction():
                    direction = np.argmax(np.array(forward_propagation(np.array([
                        is_left_blocked, is_front_blocked, is_right_blocked, 
                        fruit_direction_vector_normalized[0], snake_direction_vector_normalized[0],
                        fruit_direction_vector_normalized[1], snake_direction_vector_normalized[1]
                    ]).reshape(-1, 7), population))) - 1

                    direction = direction.tolist()

                    if direction == -1:
                        return snake.get_relative_direction('left')

                    if direction == 0: 
                        return snake.get_relative_direction(snake.direction)

                    if direction == 1:
                        return snake.get_relative_direction('right')
                    

                predicted_direction = get_direction_prediction()

                if predicted_direction == snake.direction:
                    count_same_direction += 1
                    snake.move()
                else:
                    count_same_direction = 0
                    snake.move(predicted_direction)
                
                print("[{} |_angle {}]".format(predicted_direction, angle))
                self.display_snake(snake, epoch, max_score)
                
                if not snake.is_alive():
                    reward_score += -150 # deduct
                    break
                else:
                    reward_score += 0
                
                if snake.score > max_score:
                    max_score = snake.score

                if count_same_direction > 8 and predicted_direction != snake.direction:
                    score -= 1
                else:
                    score += 2

            del snake.allspriteslist, snake.fruit, snake
            pygame.time.delay(400)

        return reward_score + score + max_score * 5_000

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
        super().__init__()

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
