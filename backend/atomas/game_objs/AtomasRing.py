
import random
from .RingElements import Atom, Plus, Minus, Root, link_two_elements, link_three_elements

class AtomasRing:


    __INIT_ATOM_COUNT = 6
    __MAX_ATOM_COUNT = 19

    __INIT_MIN_ATOM = 1
    __ATOM_RANGE = 2
    __RANGE_INCREASE_FREQUENCY = 40

    __MIN_PLUS_FREQUENCY = 5
    __MIN_MINUS_FREQUENCY = 20 

    __PLUS_PROBABILITY = 0.2
    __MINUS_PROBABILITY = 0.05


    def __init__(self):


        self.__root = Root()
        self.__score, self.__turn_count = 0, 0
        self.__min_atom, self.__atom_count = self.__INIT_MIN_ATOM, self.__INIT_ATOM_COUNT
        self.__turns_since_plus, self.__turns_since_minus = 0, 0

        self.__center_element = self.__generate_ring_element()

        # generate and set up ring
        tmp_atom = self.__root
        for _ in range(self.__INIT_ATOM_COUNT):
            new_atom = self.__generate_ring_element(include_specials = False)
            link_two_elements(tmp_atom, new_atom)
            tmp_atom = new_atom
        link_two_elements(tmp_atom, self.__root)

        self.__turns_since_plus, self.__turns_since_minus = 0, 0
        self.__is_terminal = False


    def __generate_ring_element(self, include_specials = True):

        if include_specials:

            roll = random.random()

            if self.__turns_since_plus >= self.__MIN_PLUS_FREQUENCY - 1 or roll < self.__PLUS_PROBABILITY:
                self.__turns_since_plus = 0
                self.__turns_since_minus += 1
                return Plus()

            if (self.__turns_since_minus >= self.__MIN_MINUS_FREQUENCY - 1 or roll < self.__PLUS_PROBABILITY + self.__MINUS_PROBABILITY) and self.__atom_count > 1:
                self.__turns_since_minus = 0
                self.__turns_since_plus += 1
                return Minus()
        
        if self.__min_atom > 1 and random.random() < 1/self.__atom_count:
            self.__turns_since_plus += 1
            self.__turns_since_minus += 1
            return Atom(random.randint(1, self.__min_atom - 1))

        else:
            self.__turns_since_plus += 1
            self.__turns_since_minus += 1
            return Atom(random.randint(self.__min_atom, self.__min_atom + self.__ATOM_RANGE))

    
    def __parse_input(self, index):
        try:
            index = int(index)
        except ValueError:
            raise ValueError("input index cannot be converted to int")
        if index < -1 or index > self.__atom_count:
            raise IndexError(f"input index out of range: {index} (length: {self.__atom_count})")
        return index


    def __update_atom_count(self):
        res = 0
        tmp = self.__root.get_next()
        while tmp != self.__root:
            tmp = tmp.get_next()
            res += 1
        self.__atom_count = res

 
    # circles the ring and procs the each plus it sees. starts over each time a successful proc occurs.
    # finally returns when a full loop is traversed without starting any interactions.
    def __proc_plusses(self):

        res = 0
        while(True):

            procced_score = 0
            tmp = self.__root.get_next()

            while(tmp != self.__root):
                if type(tmp) == Plus:
                    procced_score, _ = tmp.proc()
                    if procced_score:
                        break
                tmp = tmp.get_next()

            if procced_score:
                res += procced_score
            else:
                return res

    # adds the values of atoms in the ring to the score
    def __update_final_score(self):
        tmp = self.__root.get_next()
        while tmp != self.__root:
            if type(tmp) == Atom:
                self.__score += tmp.get_value()
            tmp = tmp.get_next()
            

     # TODO: Fix edge case where all atoms in the ring are combined
    def take_turn(self, index):

        # delegate input parsing
        index = self.__parse_input(index)

        # return immediately if ring is terminal
        if self.__is_terminal:
            return

        # handle transformation attempts
        if index == -1:
            if self.__center_element.is_transformable():
                self.__center_element = Plus()
            return
        
        # don't increment turn count if doing a minus pickup action
        if type(self.__center_element) != Minus:
            self.__turn_count += 1
            if self.__turn_count % self.__RANGE_INCREASE_FREQUENCY == 0:
                self.__min_atom += 1

        # insert elt into linked list
        tmp_elt = self.__root
        for i in range(index):
            tmp_elt = tmp_elt.get_next()
        new_next = tmp_elt.get_next()
        link_three_elements(tmp_elt, self.__center_element, new_next)

        # proc it and update instance variables
        self.__center_element.set_transformable(False)
        score_delta, new_center = self.__center_element.proc()
        self.__center_element = new_center
        self.__score += score_delta

        # proc any existing plusses and update atom count
        self.__score += self.__proc_plusses()
        self.__update_atom_count()

        # mark ring as terminal if atom cap is reached
        if self.__atom_count >= self.__MAX_ATOM_COUNT:
            self.__update_final_score()
            self.__is_terminal = True
            return

        # get new center element if necessary
        if not self.__center_element:
            self.__center_element = self.__generate_ring_element()


    def get_terminal(self):
        return self.__is_terminal


    def get_score(self):
        return self.__score


    def get_turn_count(self):
        return self.__turn_count


    def get_atom_count(self):
        return self.__atom_count


    def get_center_element(self):
        return self.__center_element


    def get_state(self):
        res = []
        tmp_elt = self.__root.get_next()
        while type(tmp_elt) != Root:
            res.append(tmp_elt.get_value())
            tmp_elt = tmp_elt.get_next()
        while len(res) < self.__MAX_ATOM_COUNT:
            res.append(0)
        if self.__center_element:
            res.append(self.__center_element.get_value())
        else:
            res.append(0)
        res.append(self.get_atom_count())
        return res


    # used in JSON representation
    def get_ring_str(self):
        res = ""
        tmp_elt = self.__root.get_next()
        while type(tmp_elt) != Root:
            res += str(tmp_elt.get_value()) + ","
            tmp_elt = tmp_elt.get_next()
        return res


    def __str__(self):
        res = f"\t\t\t\tCenter Element: {self.__center_element}\n\n"
        tmp = self.__root.get_next()
        res += " -- 0 -- "
        idx = 1
        while tmp != self.__root:
            res += str(tmp)
            res += f" -- {idx} -- "
            tmp = tmp.get_next()
            idx += 1
        res += "\n"
        return res

