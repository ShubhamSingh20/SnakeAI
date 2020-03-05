# Snake AI 🐍 + 🤖 + 🍎 -- Teaching Computer to play Snake using Genetic Algorithm

This project is built using pygame and utilizes Neural Networks and genetic algorithm which is used for teaching the agent (snake controller)
how to play snake.


## Game Highlights
![](docs/game.gif)


## Rewards during Game Play
Different action carries distinct, rewards and punishments are assigned for performing certain actions. Such as the following:

| Rewards   | Punishments | 
|----------|:-------------:|
| Moving towards fruit |  Moving away from fruit |
| Not dying (duh !) |    possible collison with self or boundry  |
| eating fruit | dying |
| not repeating similar move patterns| repeating moves in loop|
|covering more area| covering less area|
