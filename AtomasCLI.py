
from RingElements import Atom, Plus, Minus, Root
from AtomasRing import AtomasRing

class AtomasGame:
    
    def __init__(self):
        self._score = 0
        self._ring = AtomasRing()

    def activate(self):

        while(self._ring):
            print(self._ring)
            print("Select a Move\n> ", end = "")
            
            input_index = input()
            while(True):
                try:
                    input_index = int(input_index)
                    break
                except ValueError:
                    print("Please input an integer.")

            score_delta, self._ring = self._ring.take_turn(input_index)
            self._score += score_delta

        print(f"GAME OVER | FINAL SCORE: {self._score}")

if __name__ == "__main__":

    game = AtomasGame()
    game.activate()
