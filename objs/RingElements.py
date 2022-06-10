import math
import utils.ListUtils as ListUtils

class RingElement:

    def __init__(self):
        self.__prev = None
        self.__next = None
        self.__transformable = False

    def set_next(self, next):
        self.__next = next

    def set_prev(self, prev):
        self.__prev = prev

    def get_next(self):
        return self.__next
    
    def get_prev(self):
        return self.__prev

    def is_transformable(self):
        return self.__transformable
    
    def set_transformable(self, val):
        self.__transformable = val

    def proc(self):
        return (0, None) # (score delta, new center element)


class Atom(RingElement):

    __ID_TO_ATOM = {1 : "H", 2 : "He", 3 : "Li", 4 : "Be", 5 : "B",
            6 : "C", 7 : "N" , 8 : "O",  9 : "F" , 10 : "Ne",
            11 : "Na", 12 : "Mg", 13 : "Al", 14 : "Si", 15 : "P",
            16 : "S",  17 : "Cl", 18 : "Ar", 19 : "K" , 20 : "Ca",
            21 : "Sc", 22 : "Ti", 23 : "V" , 24 : "Cr", 25 : "Mn",
            26 : "Fe", 27 : "Co", 28 : "Ni", 29 : "Cu", 30 : "Zn",
            31 : "Ga", 32 : "Ge", 33 : "As", 34 : "Se", 35 : "Br",
            36 : "Kr", 37 : "Rb", 38 : "Sr", 39 : "Y" , 40 : "Zr",
            41 : "Nb", 42 : "Mo", 43 : "TC", 44 : "Ru", 45 : "Rh",
            46 : "Pd", 47 : "Ag", 48 : "Cd", 49 : "In", 50 : "Sn",
            51 : "Sb", 52 : "Te", 53 : "I" , 54 : "Xe", 55 : "Cs",
            56 : "Ba", 57 : "La", 58 : "Ce", 59 : "Pr", 60 : "Nd",
            61 : "Pm", 62 : "Sm", 63 : "Eu", 64 : "Gd", 65 : "Tb",
            66 : "Dy", 67 : "Ho", 68 : "Er", 69 : "Tm", 70 : "Yb",
            71 : "Lu", 72 : "Hf", 73 : "Ta", 74 : "W" , 75 : "Re",
            76 : "Os", 77 : "Ir", 78 : "Pt", 79 : "Au", 80 : "Hg",
            81 : "Tl", 82 : "Pb", 83 : "Bi", 84 : "Po", 85 : "At",
            86 : "Rn", 87 : "Fr", 88 : "Ra", 89 : "Ac", 90 : "Th",
            91 : "Pr", 92 : "U" , 93 : "Np", 94 : "Pu", 95 : "Am",
            96 : "Cm", 97 : "Bk", 98 : "Cf", 99 : "Es", 100 : "Fm"}

    def __init__(self, value):
        self.__value = value
        super().__init__()

    def get_value(self):
        return self.__value
    
    def __str__(self):
        return f"( {self.__ID_TO_ATOM[self.__value]} )"


class Plus(RingElement):
    
    def proc(self):
        
        score, num_reactions = 0, 0
        center_value = 0
        seen = {}
        prev, next = self.get_prev(), self.get_next()
        found_root, root = False, None

        while (True):


            if type(prev) == Root:
                root = prev
                prev = prev.get_prev()
                found_root = -1 # -1 indicates that root was found while traversing backwards
            elif type(next) == Root:
                root = next
                next = next.get_next()
                found_root = 1 # root was found while traversing forwards
            elif type(prev) != Atom or type(next) != Atom:
                break
            elif prev in seen or next in seen or prev == next: 
                break
            elif prev.get_value() != next.get_value():
                break
            elif num_reactions == 0: # first reaction
                num_reactions += 1
                score += math.floor(1.5 * (next.get_value() + 1)) 
                center_value = next.get_value() + 1
                next, prev = next.get_next(), prev.get_prev()
            else: # chain reaction (see atomas wiki for documentation: shorturl.at/hmzG6)
                num_reactions += 1
                multiplier = 1 + (0.5 * num_reactions)
                score += math.floor(multiplier * (center_value + 1))
                if next.get_value() >= center_value:
                    score += 2 * multiplier * (next.get_value() - center_value + 1) # apply bonus
                center_value += (next.get_value() + 2 if next.get_value() > center_value else 1)
                next, prev = next.get_next(), prev.get_prev()
            

        # add resulting element to ring and handle root node
        if num_reactions:
            new_atom = Atom(center_value)
            if found_root == 1:
                ListUtils.link_four_elements(prev, new_atom, root, next)
            elif found_root == -1:
                ListUtils.link_four_elements(prev, root, new_atom, next)
            else:
                ListUtils.link_three_elements(prev, new_atom, next)

        return (score, None)

    def __str__(self):
        return "( + )"


class Minus(RingElement):
   
    def proc(self):
        
        # new center element (res) is element after the root, unless that element is a Root
        res, prev = self.get_next(), self.get_prev()

        if type(self.get_next()) == Root:

            root = self.__next
            ListUtils.link_two_elements(prev, root)

            prev = root
            res = root.get_next()

        # extract res from ring
        new_next = res.get_next()
        ListUtils.link_two_elements(prev, new_next)
        res.set_next(None)
        res.set_prev(None)

        # extracted atom can be turned into a plus
        res.set_transformable(True)

        return (0, res)


    def __str__(self):
        return "( - )"
   

class Root(RingElement):
    pass