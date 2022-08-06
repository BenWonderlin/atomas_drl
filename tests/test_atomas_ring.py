import unittest
import random

from objs.AtomasRing import AtomasRing
from objs.RingElements import Root, Atom, Plus, Minus

class TestAtomasRing(unittest.TestCase):
    

    def init_element_chain(self, chain):
        for idx, element in enumerate(chain):
            forward_neighbor = chain[(idx + 1) % len(chain)]
            element.set_next(forward_neighbor)
            forward_neighbor.set_prev(element)


    def check_chain_completeness(self, root, num_elts):
        tmp = root
        for _ in range(num_elts):
            tmp = tmp.get_next()
        self.assertEqual( tmp, root )
        for _ in range(num_elts):
            tmp = tmp.get_prev()
        self.assertEqual( tmp, root )



    def test_ring_init(self):
        my_ring = AtomasRing()
        self.assertEqual( my_ring.get_game_state(), True )
        self.assertEqual( my_ring.get_score(), 0 )
        self.assertEqual( my_ring.get_turn_count(), 0 )
        self.assertEqual( my_ring.get_atom_count(), 6 )


    def test_plus_generation(self):
        for _ in range(32):
            my_ring = AtomasRing()
            my_ring._AtomasRing__turns_since_plus = my_ring._AtomasRing__MIN_PLUS_FREQUENCY - 1
            gen_atom = my_ring._AtomasRing__generate_ring_element(True)
            self.assertEqual( type(gen_atom), Plus )


    def test_minus_generation(self):
        for _ in range(32):
            my_ring = AtomasRing()
            my_ring._AtomasRing__turns_since_minus = my_ring._AtomasRing__MIN_MINUS_FREQUENCY - 1
            gen_atom = my_ring._AtomasRing__generate_ring_element(True)
            self.assertTrue( type(gen_atom) ==  Minus or type(gen_atom) == Plus )
    

    def test_below_min_generation(self):
        for _ in range(128):
            my_ring = AtomasRing()
            my_min_atom = random.randint(2, 100)
            my_ring._AtomasRing__min_atom = my_min_atom
            my_ring._AtomasRing__atom_count = 1
            gen_atom = my_ring._AtomasRing__generate_ring_element(False)
            self.assertTrue( gen_atom.get_value() < my_min_atom )


    def test_input_processing(self):
        my_ring = AtomasRing()
        self.assertRaises( ValueError, my_ring.take_turn, "lol" ) 
        self.assertRaises( IndexError, my_ring.take_turn, -2 ) 
        self.assertRaises( IndexError, my_ring.take_turn, 20 )
        my_ring.take_turn(-1)


    def test_atom_count(self):
        for _ in range(32):
            my_ring = AtomasRing()
            roll = random.randint(1, 12)
            for _ in range(roll):
                my_ring.take_turn(0)
            tmp = my_ring._AtomasRing__root.get_next()
            for _ in range(my_ring.get_atom_count()):
                tmp = tmp.get_next()
            self.assertEqual( tmp, my_ring._AtomasRing__root )


    def test_existing_plus(self):
        my_ring = AtomasRing()
        my_root = Root()
        my_ring._AtomasRing__root = my_root
        new_chain = self.init_element_chain(
            (my_root, Plus(), Atom(2), Atom(1))
        )
        my_ring._AtomasRing__center_element = Atom(2)
        my_ring.take_turn(0)
        self.assertEqual( my_root.get_next().get_value(), 3 )
        self.check_chain_completeness( my_root, 3 )
        

    def test_existing_plus_chain(self):
        my_ring = AtomasRing()
        my_root = Root()
        my_ring._AtomasRing__root = my_root
        new_chain = self.init_element_chain(
            (my_root, Plus(), Atom(2), Plus(), Atom(3))
        )
        my_ring._AtomasRing__center_element = Atom(2)
        my_ring.take_turn(0)
        self.assertEqual( my_root.get_next().get_value(), 4 )
        self.check_chain_completeness( my_root, 2 )


    def test_game_end(self):
        my_ring = AtomasRing()
        while (my_ring.get_game_state()):
            my_ring.take_turn(0)
        self.assertGreater( my_ring.get_score(), 0 )



if __name__ == '__main__':
    unittest.main()