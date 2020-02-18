from global_vars import COMPUTER_TRAIN
from controls import computer_play
from game import play_game_by_user

if COMPUTER_TRAIN:
    computer_play()
else:
    play_game_by_user()