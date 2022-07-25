from objs.AtomasRing import AtomasRing

class AtomasCLI:
    
    def __init__(self):
        self.__ring = AtomasRing()

    def activate(self):

        while(self.__ring.get_terminal() == False):
            print(f"\t    Turns Taken: {self.__ring.get_turn_count()}     ||     Score: {int(self.__ring.get_score())}     ||     Atom Count: {self.__ring.get_atom_count()}\n")
            print(self.__ring)
            print("Select a Move\n> ", end = "")
            
            input_index = input().strip()
            while(True):
                try:
                    input_index = int(input_index)
                    self.__ring.take_turn(input_index)
                    break
                except ValueError:
                    print("Please input an integer.\n> ", end = "")
                except IndexError:
                    print("Please input a valid index.\n> ", end = "")
                input_index = input().strip()

        print(f"GAME OVER || FINAL SCORE: {self.__ring.get_score()}")

if __name__ == "__main__":

    cli = AtomasCLI()
    cli.activate()
    
