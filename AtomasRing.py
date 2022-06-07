
import random
from RingElements import Atom, Plus, Minus, Root

class AtomasRing:


    _INIT_ATOM_COUNT = 6
    _MAX_ATOM_COUNT = 19

    _INIT_MIN_ATOM = 1
    _ATOM_RANGE = 2
    _RANGE_INCREASE_FREQUENCY = 40

    _MIN_PLUS_FREQUENCY = 5
    _MIN_MINUS_FREQUENCY = 20 

    _PLUS_PROBABILITY = 0.2
    _MINUS_PROBABILITY = 0.05


    def __init__(self):

        self._root = Root()
        self._score, self._turn_count = 0, 0
        self._min_atom = self._INIT_MIN_ATOM
        self._atom_count = self._INIT_ATOM_COUNT
        self._turns_since_plus, self._turns_since_minus = 0, 0
        self._center_element = self._generate_ring_element()

        tmp_atom = self._root
        for i in range(self._INIT_ATOM_COUNT):
            new_atom = self._generate_ring_element(include_specials = False)
            tmp_atom.set_next(new_atom)
            new_atom.set_prev(tmp_atom)
            tmp_atom = new_atom

        self._turns_since_plus, self._turns_since_minus = 0, 0
        
        tmp_atom.set_next(self._root)
        self._root.set_prev(tmp_atom)


    def _generate_ring_element(self, include_specials = True):

        if include_specials:

            roll = random.random()

            if self._turns_since_plus == self._MIN_PLUS_FREQUENCY - 1 or roll < self._PLUS_PROBABILITY:
                self._turns_since_plus = 0
                self._turns_since_minus += 1
                return Plus()

            if self._turns_since_minus == self._MIN_MINUS_FREQUENCY - 1 or roll < self._PLUS_PROBABILITY + self._MINUS_PROBABILITY:
                self._turns_since_minus = 0
                self._turns_since_plus += 1
                return Minus()
        
        if self._min_atom > 1 and random.random() < 1/self._atom_count:
            self._turns_since_plus += 1
            self._turns_since_minus += 1
            return Atom(random.randint(1, self._INIT_MIN_ATOM + 1))

        else:
            self._turns_since_plus += 1
            self._turns_since_minus += 1
            return Atom(random.randint(self._min_atom, self._min_atom + self._ATOM_RANGE))
    

    # procs plusses. if a reaction is found, the search immediately returns with the score and delta
    def _proc_plus(self):
        tmp = self._root.get_next()
        while tmp != self._root:
            if type(tmp) == Plus:
                score, new_center, atom_delta = tmp.proc()
                if score:
                    return (score, atom_delta)
            tmp = tmp.get_next()
        return (0, 0)


    def take_turn(self, index):

        if index < -1 or index > self._atom_count:
            return(0, self)

        if index == -1:
            if self._center_element.can_transform():
                self._center_element = Plus()
                return (0, self)
            else:
                return (0, self)
        
        if type(self._center_element) != Minus: # don't increment turn count if doing a minus pickup action
            self._turn_count += 1
            if self._turn_count == self._RANGE_INCREASE_FREQUENCY:
                self._min_atom += 1

        # insert elt into linked list
        tmp_elt = self._root
        for i in range(index):
            tmp_elt = tmp_elt.get_next()
        new_next = tmp_elt.get_next()
        new_next.set_prev(self._center_element)
        self._center_element.set_next(new_next)
        self._center_element.set_prev(tmp_elt)
        tmp_elt.set_next(self._center_element)

        # proc it and return score
        self._center_element.set_transform(False)
        score_delta, new_center, atom_delta = self._center_element.proc()
        self._center_element = new_center
        if not self._center_element:
            self._center_element = self._generate_ring_element()
        self._atom_count += atom_delta

        # keep proccing plusses until full loop is made around ring w/o a reacion
        while(True):
            plus_score, plus_delta = self._proc_plus()
            if plus_score:
                score_delta += plus_score
                self._atom_count += plus_delta
            else:
                break

        # return None if ring is full
        if self._atom_count >= self._MAX_ATOM_COUNT:
            self._score += score_delta
            return(score_delta, None)

        self._score += score_delta
        return (score_delta, self)


    def __str__(self):
        res = f"\n\tRing Length: {self._atom_count}     ||     SCORE: {self._score}     ||     Turns Taken: {self._turn_count}\n\n"
        res += f"\t\t\t   Center Element: {self._center_element}\n\n"
        tmp = self._root.get_next()
        res += " -- 0 -- "
        idx = 1
        while tmp != self._root:
            res += str(tmp)
            res += f" -- {idx} -- "
            tmp = tmp.get_next()
            idx += 1
        res += "\n"
        return res

