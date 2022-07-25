import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from objs.AtomasRing import AtomasRing


class AtomasWrapper:
    

    __TRANSFORM_IDX = 18
    __NUM_ACTIONS = 19
    __INACTION_REWARD = -1


    def __init__(self):
        self.__ring = AtomasRing()


    def check(self):
        return ( self.__ring.get_state(), 0, self.__ring.get_terminal() )


    def step(self, action_vec):

        # action vec is a 19 x 1 one-hot encoded vector
        # where the first 18 indices correspond to the ring's edge indices
        # and the last corresponds to tapping the center (i.e., a transform attempt)

        action_idx = tf.argmax(action_vec)

        if action_idx < 0 or (action_idx >= self.__ring.get_atom_count() and action_idx != self.__TRANSFORM_IDX): # self.__ring.get_terminal() or
            return ( self.__ring.get_state(), self.__INACTION_REWARD, False )

        if action_idx == self.__TRANSFORM_IDX:
            action_idx = -1

        prev_score = self.__ring.get_score()
        self.__ring.take_turn(action_idx)

        new_state = self.__ring.get_state()
        reward = self.__ring.get_score() - prev_score
        terminal = self.__ring.get_terminal()

        return ( new_state, reward, terminal )


    def activate(self):

        model = keras.models.load_model("first_model")
        current_state, _, _ = self.check()

        while(not self.__ring.get_terminal()):

            print(f"\n\t    Turns Taken: {self.__ring.get_turn_count()}     ||     Score: {int(self.__ring.get_score())}     ||     Atom Count: {self.__ring.get_atom_count()}\n")
            print(self.__ring)
            print("Select a Move\n> ", end = "")
                     
            current_state_tensor = tf.convert_to_tensor(current_state)
            current_state_tensor = tf.expand_dims(current_state_tensor, 0)
            q_value = model(current_state_tensor, training = False)

            action_idx = tf.argmax(q_value[0]).numpy()
            action_vec = np.zeros(self.__NUM_ACTIONS)
            action_vec[action_idx] = 1

            prev_state, _, _ = self.check()
            next_state, reward, _ = self.step(action_vec)

            if prev_state == next_state:
                action_vec = np.zeros(self.__NUM_ACTIONS)
                action_vec[0] = 1
                _, reward, _ = self.step(action_vec)
                print(f"{action_idx}->0, Reward: {reward}")
            else:
                print(f"{action_idx}, Reward: {reward}")
   

        print(f"\nGAME OVER || FINAL SCORE: {self.__ring.get_score()}")

        
