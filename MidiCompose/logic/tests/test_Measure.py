import numpy as np
import pytest
from numpy.testing import assert_array_equal

from MidiCompose.logic.rhythm import Beat, Measure, TimeUnit
from MidiCompose.logic.tests import TEST_CONSTANTS as TC

@pytest.mark.parametrize(["measure_object","expected_state"],
                         [
                             (TC.m1,TC.m1_st)
                         ])
def test_Measure_state_refactor(measure_object,expected_state):
    assert_array_equal(measure_object.state,expected_state)

# TODO
def test_Measure_constructor():
    pass

# TODO
def test_Measure_constructor_fails():
    pass


def test_Measure_iterator():
    measure = Measure(beats=[
        Beat(3),
        Beat([1, 1, 0]),
        Beat(4)
    ])
    for beat in measure:
        assert type(beat) == Beat


def test_Measure_indexing():
    measure = Measure(beats=[
        Beat(3),
        Beat([1, 1, 0]),
        Beat(4)
    ])
    assert measure[0].subdivision == 3

    assert measure[1].subdivision == 3
    assert measure.beats[0].time_units[0] == 0
    assert measure.beats[-1].time_units[0] == 0

    assert measure[2].subdivision == 4

# TODO
def test_Measure_set_state():
    m = Measure([[1,2],
                [1,2]])
    m.set_state(state=[[1,2,2],[1,2,2]])

    assert m.state[0] == -2
    assert m.state[1] == -3
    assert m.state[2] == 3

def test_n_time_units():
    m = Measure([Beat(4),[1,2,2,1]])

    assert m.n_time_units == 8

