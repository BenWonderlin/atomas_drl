
import numpy as np
import tensorflow as tf
from tensorflow import keras
from game_objs.AtomasRing import AtomasRing


class AtomasWrapper:
    
    __TERMINAL_REWARD = -10
    __NUM_ACTIONS = 18


    def __init__(self):
        self.__ring = AtomasRing()


    def check(self):
        return ( self.__ring.get_state(), self.__ring.get_atom_count(), 0, self.__ring.get_terminal() )


    def step(self, action_vec):

        # action vec is a 18 x 1 one-hot encoded vector
        # where the 18 indices correspond to the ring's edge indices

        action_idx = tf.argmax(action_vec)
        prev_score = self.__ring.get_score()
        self.__ring.take_turn(action_idx)

        new_state = self.__ring.get_state()
        num_legal_actions = self.__ring.get_atom_count()
        terminal = self.__ring.get_terminal()
        reward = self.__TERMINAL_REWARD if terminal else self.__ring.get_score() - prev_score


        return ( new_state, num_legal_actions, reward, terminal )


    def activate(self):
        
        model = keras.models.load_model("dqn_model")

        while(not self.__ring.get_terminal()):

            current_state, num_legal_actions, _, _ = self.check()

            print(f"\n\t    Turns Taken: {self.__ring.get_turn_count()}     ||     Score: {int(self.__ring.get_score())}     ||     Atom Count: {self.__ring.get_atom_count()}\n")
            print(self.__ring)
            print("Select a Move\n> ", end = "")
                     
            current_state_tensor = tf.convert_to_tensor(current_state)
            current_state_tensor = tf.expand_dims(current_state_tensor, 0)
            q_values = model(current_state_tensor, training = False)

            action_idx = tf.argmax(q_values[0][:num_legal_actions]).numpy()
            action_vec = np.zeros(self.__NUM_ACTIONS)
            action_vec[action_idx] = 1

            _, _, reward, _ = self.step(action_vec)

            print(f"{action_idx}, Reward: {reward}")
   

        print(f"\nGAME OVER || FINAL SCORE: {self.__ring.get_score()}")

        
if __name__ == "__main__":
    
    scores = []
    model = keras.models.load_model("dqn_model")
    for i in range(0, 100):
        wrapper = AtomasWrapper()
        wrapper.activate()
        scores.append(wrapper._AtomasWrapper__ring.get_score())
    print(np.mean(scores))