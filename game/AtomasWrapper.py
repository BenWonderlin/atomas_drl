import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from objs.AtomasRing import AtomasRing


class AtomasWrapper:
    

    __INACTION_REWARD = -1
    __TERMINAL_REWARD = -10
    __NUM_ACTIONS = 18


    def __init__(self):
        self.__ring = AtomasRing()


    def check(self):
        return ( self.__ring.get_state(), 0, self.__ring.get_terminal() )


    def step(self, action_vec):

        # action vec is a 18 x 1 one-hot encoded vector
        # where the 18 indices correspond to the ring's edge indices

        action_idx = tf.argmax(action_vec)

        if action_idx < 0 or (action_idx >= self.__ring.get_atom_count() and (self.__ring.get_atom_count() != 0 or action_idx != 0)):
            # if self.__ring.get_atom_count() <= 1: 
            #     print(f"Invalid action: {action_idx} on ring size {self.__ring.get_atom_count()}")
            #     print(self.__ring)
            return ( self.__ring.get_state(), self.__INACTION_REWARD, False )

        prev_score = self.__ring.get_score()
        self.__ring.take_turn(action_idx)

        new_state = self.__ring.get_state()
        terminal = self.__ring.get_terminal()
        reward = self.__TERMINAL_REWARD if terminal else self.__ring.get_score() - prev_score

        return ( new_state, reward, terminal )


    def activate(self):
        
        model = keras.models.load_model("third_model")

        while(not self.__ring.get_terminal()):

            current_state, _, _ = self.check()

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
            next_state, first_reward, _ = self.step(action_vec)

            if prev_state == next_state:
                action_vec = np.zeros(self.__NUM_ACTIONS)
                action_vec[0] = 1
                _, second_reward, _ = self.step(action_vec)
                print(f"{action_idx}->0, Reward: {first_reward}->{second_reward}")
            else:
                print(f"{action_idx}, Reward: {first_reward}")
   

        print(f"\nGAME OVER || FINAL SCORE: {self.__ring.get_score()}")

        
