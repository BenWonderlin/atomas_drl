from objs.AtomasRing import AtomasRing

class AtomasWrapper:
    
    def __init__(self):
        self.__ring = AtomasRing()

    def step(self, action):
        # not using the last (duplicate) index for selection to simplify Q network
        # -1 still represents a transform action
        if action < -1 or action >= self.__ring.get_atom_count():
            raise IndexError("Not a valid index into ring")

        prev_score = self.__ring.get_score()
        self.__ring.take_turn(action)

        new_state = self.__ring.get_state_list()
        reward = self.__ring.get_score() - prev_score
        terminal = self.__ring.get_terminal()

        return (new_state, reward, terminal)
        
