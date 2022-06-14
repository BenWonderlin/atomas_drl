
import unittest

from utils.ListUtils import init_element_chain, check_chain_completeness
from objs.RingElements import Root, Atom, Plus, Minus 

class TestRingElements(unittest.TestCase):


    # sets up a prev/next pointers from a chain of elements
    def init_element_chain(self, chain):
        for idx, element in enumerate(chain):
            forward_neighbor = chain[(idx + 1) % len(chain)]
            element.set_next(forward_neighbor)
            forward_neighbor.set_prev(element)

    # checks that prev/next pointers form a ring
    def check_chain_completeness(self, root, num_elts):
        tmp = root
        for _ in range(num_elts):
            tmp = tmp.get_next()
        self.assertEqual( tmp, root )
        for _ in range(num_elts):
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


    # full-ring reaction
    def test_plus_proc_seen(self):
        my_root, my_plus = Root(), Plus()
        self.init_element_chain(
            (my_root, Atom(1), my_plus, Atom(1), Atom(3), Atom(3))
        )
        score, new_center = my_plus.proc()
        self.assertEqual( score, 17 )
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



if __name__ == '__main__':
    unittest.main()