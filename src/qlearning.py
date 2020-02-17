from global_vars import Q_LEARN, Screen
import numpy as np
import pickle

def get_q_table():
    q_table = {}

    if Q_LEARN.Q_TABLE_FILENAME is None:
        for x1 in range(Screen.SCREEN_WIDTH):
            for y1 in range(Screen.SCREEN_HEIGTH):
                q_table[(x1, y1)] = [ 
                    np.random.uniform(-5, 0) for i in range(Q_LEARN.ACTION_SIZE)
                ]
    else:
        with open(Q_LEARN.Q_TABLE_FILENAME, 'rb') as afile:
            q_table = pickle.load(afile)
    
    return q_table