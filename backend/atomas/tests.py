import unittest
import random

from game_objs.AtomasRing import AtomasRing
from game_objs.RingElements import Root, Atom, Plus, Minus


class TestRingElements(unittest.TestCase):


    # utility function that sets up a prev/next pointers from a chain of elements
    def init_element_chain(self, chain):
        for idx, element in enumerate(chain):
            forward_neighbor = chain[(idx + 1) % len(chain)]
            element.set_next(forward_neighbor)
            forward_neighbor.set_prev(element)

    # utility function that checks that prev/next pointers form a non-cyclic ring
    def check_chain_completeness(self, root, num_elts):

        tmp = root

        # forward links
        seen = set()
        for _ in range(num_elts):
            self.assertFalse( tmp in seen )
            seen.add(tmp)
            tmp = tmp.get_next()
        self.assertEqual( tmp, root )

        # backward links
        seen = set()
        for _ in range(num_elts):
            self.assertFalse( tmp in seen )
            seen.add(tmp)
            tmp = tmp.get_prev()
        self.assertEqual( tmp, root )


    def test_atom_init(self):
        dummy_atom = Atom(69)
        self.assertEqual( dummy_atom.get_value(), 69 )
        self.assertEqual( str(dummy_atom), "( Tm )" )
        self.assertIsNone( dummy_atom.get_prev() )
        self.assertIsNone( dummy_atom.get_next() )
        self.assertFalse( dummy_atom.is_transformable() )


    # tests forward and backward links
    def test_element_chain(self):
        my_root = Root()
        self.init_element_chain(
            (my_root, Atom(14), Plus(), Minus())
        )
        tmp = my_root
        for _ in range(4):
            tmp = tmp.get_next()
        self.assertEqual( tmp, my_root )
        for _ in range(4):
            tmp = tmp.get_prev()
        self.assertEqual( tmp, my_root )
    

    def test_plus_proc_simple(self):
        my_root, my_plus = Root(), Plus()
        self.init_element_chain(
            (my_root, Atom(2), my_plus, Atom(2), Atom(1))
        )
        score, new_center = my_plus.proc()
        self.assertEqual( score, 4 )
        self.assertIsNone( new_center )
        self.assertEqual( my_root.get_next().get_value(), 3 )


    # corner case where prev and next seekers first meet on the Root
    def test_plus_proc_perfect_fold(self):
        my_root, my_plus = Root(), Plus()
        self.init_element_chain(
            (my_root, Atom(1), my_plus, Atom(1))
        )
        score, new_center = my_plus.proc()
        self.assertEqual( score, 3 )
        self.assertIsNone( new_center )
        self.assertEqual( my_root.get_next().get_value(), 2)
        self.check_chain_completeness( my_root, 2 )


    # example case given on atomas wiki's score page
    def test_plus_proc_chain_reaction(self):
        my_root, my_plus = Root(), Plus()
        self.init_element_chain(
            (my_root, 
             Atom(2), Atom(1), Atom(2), Atom(3), Atom(1),
             my_plus,
             Atom(1), Atom(3), Atom(2), Atom(1), Atom(2),
             Atom(5))
        )
        score, new_center = my_plus.proc()
        self.assertEqual( score, 81 )
        self.assertIsNone( new_center ) 
        self.assertEqual( my_root.get_next().get_value(), 8 )
        self.check_chain_completeness( my_root, 3 )


    # small full-ring reaction
    def test_plus_proc_small(self):
        my_root, my_plus = Root(), Plus()
        self.init_element_chain(
            (my_root, Atom(1), my_plus, Atom(1), Atom(3), Atom(3))
        )
        score, new_center = my_plus.proc()
        self.assertEqual( score, 17 )
        self.assertIsNone( new_center )
        self.assertEqual( my_root.get_next().get_value(), 5)
        self.check_chain_completeness( my_root, 2 )


    # large full-ring reaction initiated from location across from root
    def test_plus_proc_large(self):
        my_root, my_plus = Root(), Plus()
        self.init_element_chain(
            (my_root, Atom(1), Atom(3), Atom(3), Atom(1), Atom(1), my_plus, Atom(1))
        )
        _, new_center = my_plus.proc()
        self.assertIsNone( new_center )
        self.assertEqual( my_root.get_next().get_value(), 5)
        self.check_chain_completeness( my_root, 2 )
    
    
    # corner case where reaction is broken by two adjacent nodes, one of which is the root
    def test_plus_proc_adjacent(self):
        my_root, my_plus = Root(), Plus()
        self.init_element_chain(
            (my_root, Atom(3), Atom(1), my_plus, Atom(1), Atom(3), Atom(5))
        )
        score, new_center = my_plus.proc()
        self.assertEqual( score, 17 )
        self.assertIsNone( new_center )
        self.assertEqual( my_root.get_next().get_value(), 5)
        self.assertEqual( my_root.get_prev().get_value(), 5)
        self.check_chain_completeness( my_root, 3 )


    # next two tests check that the atom produced from a reaction is
    # placed correctly relative to root node
    def test_plus_proc_root_forward(self):
        my_root, my_plus = Root(), Plus()
        self.init_element_chain(
            (Atom(3), Atom(1), my_plus, my_root, Atom(1))
        )
        score, new_center = my_plus.proc()
        self.assertEqual( score, 3 )
        self.assertIsNone( new_center )
        self.assertEqual( my_root.get_prev().get_value(), 2 )
        self.assertEqual( my_root.get_next().get_value(), 3 )
        self.check_chain_completeness( my_root, 3 )


    def test_plus_proc_root_backward(self):
        my_root, my_plus = Root(), Plus()
        self.init_element_chain(
            (Atom(3), Atom(1), my_root, my_plus, Atom(1))
        )
        score, new_center = my_plus.proc()
        self.assertEqual( score, 3 )
        self.assertIsNone( new_center )
        self.assertEqual( my_root.get_prev().get_value(), 3 )
        self.assertEqual( my_root.get_next().get_value(), 2 )
        self.check_chain_completeness( my_root, 3 )


    def test_minus_proc_simple(self):
        my_root, my_minus = Root(), Minus()
        my_atom = Atom(3)
        self.init_element_chain(
            (my_root, my_minus, my_atom, Atom(1))
        )
        score, new_center = my_minus.proc()
        self.assertEqual( score, 0 )
        self.assertEqual( new_center, my_atom )
        self.assertTrue( new_center.is_transformable() )
        self.assertEqual( my_root.get_next().get_value(), 1 )
        self.check_chain_completeness( my_root, 2 )


    # case where minus is placed right before root
    def test_minus_proc_root(self):
        my_root, my_minus = Root(), Minus()
        my_atom = Atom(3)
        self.init_element_chain(
            (my_minus, my_root, my_atom, Atom(1))
        )
        score, new_center = my_minus.proc()
        self.assertEqual( score, 0 )
        self.assertEqual( new_center, my_atom )
        self.assertTrue( new_center.is_transformable() )
        self.assertEqual( my_root.get_next().get_value(), 1 )
        self.check_chain_completeness( my_root, 2 )






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
        self.assertEqual( my_ring.get_terminal(), False )
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
        while (my_ring.get_terminal() == False):
            my_ring.take_turn(0)
        self.assertGreater( my_ring.get_score(), 0 )



if __name__ == '__main__':
    unittest.main()