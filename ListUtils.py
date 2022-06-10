
def link_two_elements(one, two):
    one.set_next(two)
    two.set_prev(one)

def link_three_elements(one, two, three):
    one.set_next(two)
    two.set_prev(one)
    two.set_next(three)
    three.set_prev(two)

def link_four_elements(one, two, three, four):
    one.set_next(two)
    two.set_prev(one)
    two.set_next(three)
    three.set_prev(two)
    three.set_next(four)
    four.set_prev(three)