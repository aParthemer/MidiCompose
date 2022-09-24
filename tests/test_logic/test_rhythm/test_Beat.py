import numpy as np
from numpy.testing import assert_array_equal

from MidiCompose.logic.rhythm.time_unit import TimeUnit
from MidiCompose.logic.rhythm.beat import Beat

#### PROPERTIES ####
def test_constructor():
    constructor_args = [
        4,
        [1,2,0,0],
        [TimeUnit(0),TimeUnit(1)]
    ]
    for a in constructor_args:
        b = Beat(a)

        assert type(b.time_units) == list
        assert type(b.time_units[0]) == TimeUnit

        assert type(b.state) == np.ndarray
        assert type(b.state[0]) == np.int8

def test_state():
    b = Beat([1,0,1,2])
    expected_st = np.array([-3,4,1,0,1,2])
    assert_array_equal(b.state,expected_st)

def test_subdivision():

    b = Beat([1,0,0,0])

    assert b.subdivision == 4


def test_iterator():
    b = Beat(4)

    for tu in b:
        assert type(tu) == TimeUnit


def test_indexing():

    b = Beat([0, 1, 2, 0])
    assert type(b[0]) == np.int8
    assert type(b.time_units[0]) == TimeUnit
    assert b[3] == 0


def test_mul():

    b = Beat([1, 2, 0])
    beats = b * 2

    for b_copy in beats:
        assert b_copy.subdivision == 3
        assert type(b_copy[0]) == np.int8
        assert b_copy.time_units[0] == 1


def test_set_state():
    b = Beat([1,2,1,2])

    expected_st = np.array([-3,4,1,2,1,2])

    assert_array_equal(b.state,expected_st)
    assert b.time_units == [TimeUnit(1),TimeUnit(2),TimeUnit(1),TimeUnit(2)]

    # alter figure
    b.set_state([0,1,2,2,1])

    expected_st = np.array([-3, 5, 0, 1, 2, 2, 1])

    assert_array_equal(b.state, expected_st)
    assert b.time_units == [TimeUnit(0), TimeUnit(1), TimeUnit(2), TimeUnit(2), TimeUnit(1)]

#### UTILITY METHODS ####

def test_activate_random():
    b = Beat(8)
    assert {0}.issuperset(set([tu.state for tu in b.time_units]))

    n_tries = 10
    previous = []
    for _ in range(n_tries):
        previous.append(b.activate_random(density=.9,random_seed=1))

        assert 1 in b.state

def test_sustain_all():
    b = Beat([1,0,1,0,0,0])
    b.sustain_all()
    assert_array_equal(b.state,np.array([-3,6,  1,2,1,2,2,2]))

def test_short_all():
    b = Beat([1,2,2,1,2,2,1,0])
    b.shorten_all()
    assert_array_equal(b.state,np.array([-3,8,  1,0,0,1,0,0,1,0]))

