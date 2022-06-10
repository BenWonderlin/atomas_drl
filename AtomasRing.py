
import random
from RingElements import Atom, Plus, Minus, Root
import ListUtils

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
        self._min_atom, self._atom_count = self._INIT_MIN_ATOM, self._INIT_ATOM_COUNT
        self._turns_since_plus, self._turns_since_minus = 0, 0

        self._center_element = self._generate_ring_element()

        # generate and set up ring
        tmp_atom = self._root
        for i in range(self._INIT_ATOM_COUNT):
            new_atom = self._generate_ring_element(include_specials = False)
            ListUtils.link_two_elements(tmp_atom, new_atom)
            tmp_atom = new_atom
        ListUtils.link_two_elements(tmp_atom, self._root)

        self._turns_since_plus, self._turns_since_minus = 0, 0
        self._is_playable = True


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

    
    def _parse_input(self, index):
        try:
            index = int(index)
        except ValueError:
            raise ValueError("input index cannot be converted to int")
        if index < -1 or index > self._atom_count:
            raise IndexError("input index out of range")
        return index


    def _update_atom_count(self):
        res = 0
        tmp = self._root.get_next()
        while tmp != self._root:
            tmp = tmp.get_next()
            res += 1
        self._atom_count = res

 
    # circles the ring and procs the each plus it sees. starts over each time a successful proc occurs.
    # finally returns when a full loop is traversed without starting any interactions.
    def _proc_plusses(self):

        res = 0
        while(True):

            procced_score = 0
            tmp = self._root.get_next()

            while(tmp != self._root):
                if type(tmp) == Plus:
                    procced_score, _ = tmp.proc()
                    if procced_score:
                        break
                tmp = tmp.get_next()

            if procced_score:
                res += procced_score
            else:
                return res


    def take_turn(self, index):

        # delegate input parsing
        index = self._parse_input(index)

        # return immediately if ring is unplayable
        if not self._is_playable:
            return

        # handle transformation attempts
        if index == -1:
            if self._center_element.can_transform():
                self._center_element = Plus()
            return
        
        # don't increment turn count if doing a minus pickup action
        if type(self._center_element) != Minus:
            self._turn_count += 1
            if self._turn_count == self._RANGE_INCREASE_FREQUENCY:
                self._min_atom += 1

        # insert elt into linked list
        tmp_elt = self._root
        for i in range(index):
            tmp_elt = tmp_elt.get_next()
        new_next = tmp_elt.get_next()
        ListUtils.link_three_elements(tmp_elt, self._center_element, new_next)

        # proc it and update instance variables
        self._center_element.set_transformable(False)
        score_delta, new_center = self._center_element.proc()
        self._center_element = new_center
        self._score += score_delta

        # proc any existing plusses and update atom count
        self._score += self._proc_plusses()
        self._update_atom_count()

        # get new center element if necessary
        if not self._center_element:
            self._center_element = self._generate_ring_element()

        # mark ring as unplayable if atom cap is reached
        if self._atom_count >= self._MAX_ATOM_COUNT:
            self._is_playable = False


    def get_game_state(self):
        return self._is_playable


    def get_score(self):
        return self._score


    def get_turn_count(self):
        return self._turn_count


    def get_atom_count(self):
        return self._atom_count

    
    def __str__(self):
        res = f"\t\t\t\tCenter Element: {self._center_element}\n\n"
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

