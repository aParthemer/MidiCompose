from typing import List

import pytest

import numpy as np
from icecream import ic

from MidiCompose.logic.rhythm import TimeUnit, Beat, Measure


#### TimeUnit ####

def test_TimeUnit_constructor():
    tu = TimeUnit()
    assert tu.state == 0

    tu.activate()
    assert tu.state == 1

    tu.sustain()
    assert tu.state == 2

    tu.deactivate()
    assert tu.state == 0

    with pytest.raises(TypeError):
        invalid = ["1", 1.1]

        [TimeUnit(a) for a in invalid]

    with pytest.raises(ValueError):
        invalid = [-1, 3]
        [TimeUnit(a) for a in invalid]


def test_TimeUnit_equality():
    tu = TimeUnit(1)
    assert tu.state == 1
    assert tu == 1

    assert TimeUnit(0) == TimeUnit(0).state == 0


def test_TimeUnit_integer():
    tu = TimeUnit(1)
    assert type(int(tu)) == int


#### Beat ####

def test_Beat_constructor_given_subdivision():
    b = Beat(4)

    assert b.subdivision == 4
    assert type(b.state) == np.ndarray
    assert type(b[0]) == np.int64
    assert type(b.time_units) == np.ndarray
    assert type(b.time_units[0]) == TimeUnit

    assert b.state.ndim == 1

    # all TimeUnit instances have `time_units` == 0
    assert set([int(tu) for tu in b.time_units]).issubset({0})

    with pytest.raises(TypeError):
        Beat("1")
    with pytest.raises(ValueError):
        invalid = [0, -1]
        [Beat(a) for a in invalid]


def test_Beat_constructor_given_iterable():
    b = Beat([1, 0, 1, 2])

    assert b.subdivision == 4
    assert type(b.state) == np.ndarray
    assert b.state.ndim == 1
    assert b[0] == 1
    assert b[-1] == 2

    b = Beat([TimeUnit(0), 1, 2])

    assert b.subdivision == 3
    assert type(b.state) == np.ndarray
    assert b.state.ndim == 1

    with pytest.raises(TypeError):
        invalid = [
            "1012",
            [1, 0, "1", 2]
        ]
        [Beat(a) for a in invalid]

    with pytest.raises(ValueError):
        invalid = [
            [1, 2, 3],
            [0, -1]
        ]
        [Beat(a) for a in invalid]


def test_Beat_iterator():
    b = Beat(4)

    for tu in b:
        assert type(tu) == TimeUnit


def test_Beat_indexing():
    b = Beat([0, 1, 2, 0])
    assert type(b[0]) == np.int64
    assert type(b.time_units[0]) == TimeUnit
    assert b[3] == 0


def test_Beat_mul():
    b = Beat([1, 2, 0])
    beats = b * 2

    for b_copy in beats:
        assert b_copy.subdivision == 3
        assert type(b_copy[0]) == np.int64
        assert b_copy.time_units[0] == 1

# TODO
def test_Beat_set_state():
    pass

#### Measure ####

def test_Measure_constructor():

    # given Beat instances
    beats = [Beat(4), Beat([1,1,1,2])]
    m = Measure(beats=beats)
    assert type(m.state) == np.ndarray
    assert type(m.state[0]) == np.ndarray
    assert type(m.state[0][0]) == np.int64

    assert type(m.beats) == np.ndarray
    assert type(m.beats[0]) == Beat
    assert m.n_beats == 2
    assert m.state[0][0] == 0
    assert m.state[1][0] == 1

    # given collection of collections
    beats = [
        [0,2],
        [2,1]
    ]
    m = Measure(beats=beats)
    assert m.state[0][0] == 0
    assert m.state[1][0] == 2

def test_Measure_constructor_given_mixture():
    # time_units = (4,Beat,5)
    # Measure(time_units)
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


def test_Measure_set_state():
    m = Measure([[1,2],
                [1,2]])
    assert m.state[0][0] == 1
    assert m.state[1][1] == 2
    assert type(m.state[0]) == np.ndarray
    assert type(m.state[0][0]) == np.int64
    assert type(m.beats[0]) == Beat
    assert type(m.beats[0].time_units[0]) == TimeUnit

    m.set_state([[0,1],[2,1]])

    assert m.state[0][0] == 0
    assert m.state[1][1] == 1
    assert type(m.state[0]) == np.ndarray
    assert type(m.state[0][0]) == np.int64
    assert type(m.beats[0]) == Beat
    assert type(m.beats[0].time_units[0]) == TimeUnit

# TODO
def test_Measure_set_state_fails():
    pass


