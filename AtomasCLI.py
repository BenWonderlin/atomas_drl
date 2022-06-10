from AtomasRing import AtomasRing

class AtomasCLI:
    
    def __init__(self):
        self._ring = AtomasRing()

    def activate(self):

        while(self._ring.get_game_state()):
            print(f"\t    Turns Taken: {self._ring.get_turn_count()}     ||     Score: {self._ring.get_score()}     ||     Atom Count: {self._ring.get_atom_count()}\n")
            print(self._ring)
            print("Select a Move\n> ", end = "")
            
            input_index = input()
            while(True):
                try:
                    input_index = int(input_index)
                    break
                except ValueError:
                    print("Please input an integer.")

            self._ring.take_turn(input_index)

        print(f"GAME OVER | FINAL SCORE: {self._score}")

if __name__ == "__main__":

    cli = AtomasCLI()
    cli.activate()
