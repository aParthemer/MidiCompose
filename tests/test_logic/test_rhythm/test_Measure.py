import numpy as np
import pytest
from numpy.testing import assert_array_equal

from MidiCompose.logic.rhythm.beat import Beat
from MidiCompose.logic.rhythm.measure import Measure


def test_Measure_constructor():
    m = Measure()
    assert m.n_beats == 1
    assert m.n_note_on == 0


def test_Measure_iterator():
    measure = Measure(beats=[
        Beat(3),
        Beat([1, 1, 0]),
        Beat(4)
    ])
    for beat in measure:
        assert type(beat) == Beat


def test_indexing():
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
def test_set_state():
    m = Measure([[1, 2],
                 [1, 2]])
    m.set_state(state=[[1, 2, 2], [1, 2, 2]])

    assert m.state[0] == -2
    assert m.state[1] == -3
    assert m.state[2] == 3


#### UTILITY METHODS ####

def test_sustain_all():
    m = Measure([Beat([1, 0, 0, 1]), Beat([0, 1, 0, 1, 0, 0])])
    expected_st = np.array([-2,
                            -3, 4, 1, 2, 2, 1,
                            -3, 6, 2, 1, 2, 1, 2, 2])
    m.sustain_all()
    assert_array_equal(m.state, expected_st)

    # with index selection
    m = Measure([Beat([1, 0, 0, 1]), Beat([0, 1, 0, 1, 0, 0])])
    expected_st = np.array([-2,
                            -3, 4, 1, 0, 0, 1,
                            -3, 6, 2, 1, 2, 1, 2, 2])
    m.sustain_all(beat_idx=[1])
    assert_array_equal(m.state, expected_st)


# TODO
def test_shorten_all():
    pass


