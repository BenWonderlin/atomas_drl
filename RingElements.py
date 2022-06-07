import math

class RingElement:

    def __init__(self):
        self._prev = None
        self._next = None
        self._can_transform = False

    def set_next(self, next):
        self._next = next

    def set_prev(self, prev):
        self._prev = prev

    def get_next(self):
        return self._next
    
    def get_prev(self):
        return self._prev

    def can_transform(self):
        return self._can_transform
    
    def set_transform(self, val):
        self._can_transform = val

    def proc(self):
        return (0, None, 1)

    def _link_three_elements(self, one, two, three):
        one.set_next(two)
        two.set_prev(one)
        two.set_next(three)
        three.set_prev(two)

    def _link_four_elements(self, one, two, three, four):
        one.set_next(two)
        two.set_prev(one)
        two.set_next(three)
        three.set_prev(two)
        three.set_next(four)
        four.set_prev(three)


class Atom(RingElement):

    _ID_TO_ATOM = {1 : "H", 2 : "He", 3 : "Li", 4 : "Be", 5 : "B",
            6 : "C", 7 : "N" , 8 : "O",  9 : "F" , 10 : "Ne",
            11 : "Na", 12 : "Mg", 13 : "Al", 14 : "Si", 15 : "P",
            16 : "S",  17 : "Cl", 18 : "Ar", 19 : "K" , 20 : "Ca",
            21 : "Sc", 22 : "Ti", 23 : "V" , 24 : "Cr", 25 : "Mn"}

    def __init__(self, value):
        self.value = value
        super().__init__()
    
    def __str__(self):
        return f"( {self._ID_TO_ATOM[self.value]} )"

# test comment

class Plus(RingElement):
    
    def proc(self):
        
        score, num_reactions = 0, 0
        center_value = 0
        seen = {}
        prev, next = self._prev, self._next
        found_root, root = False, None

        while (True):

            if type(prev) == Root:
                root = prev
                prev = prev.get_prev()
                found_root = -1
            elif type(next) == Root:
                root = next
                next = next.get_next()
                found_root = 1
            elif type(prev) != Atom or type(next) != Atom:
                break
            elif prev in seen or next in seen or prev == next:
                break
            elif prev.value != next.value:
                break
            elif num_reactions == 0: # first reaction
                num_reactions += 1
                score += math.floor(1.5 * (next.value + 1)) 
                center_value = next.value + 1
                next, prev = next.get_next(), prev.get_prev()
            else: # chain reaction
                num_reactions += 1
                multiplier = 1 + 0.5 * num_reactions
                score += math.floor(multiplier * (center_value + 1))  # from atomas wiki
                if next.value >= center_value:
                    score += 2 * multiplier * (next.value - center_value + 1)
                center_value += (next.value + 2 if next.value > center_value else 1)
                next, prev = next.get_next(), prev.get_prev()

        if num_reactions:
            new_atom = Atom(center_value)
            if found_root == 1:
                self._link_four_elements(prev, new_atom, root, next)
            elif found_root == -1:
                self._link_four_elements(prev, root, new_atom, next)
            else:
                self._link_three_elements(prev, new_atom, next)

        return (score, None, 1 - 2 * num_reactions)

    def __str__(self):
        return "( + )"


class Minus(RingElement):
   
    def proc(self):

        res = self._next
        prev = self._prev

        if type(self._next) == Root:

            root = self._next
            prev.set_next(root)
            root.set_prev(prev)

            prev = root
            res = root.get_next()

        new_next = res.get_next()
        prev.set_next(new_next)
        new_next.set_prev(prev)

        res.set_next(None)
        res.set_prev(None)
        res.set_transform(True)

        return (0, res, -1)

    def __str__(self):
        return "( - )"
   

class Root(RingElement):
    pass