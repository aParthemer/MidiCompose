from typing import List

import pytest

import numpy as np
from icecream import ic

from MidiCompose.logic.rhythm import TimeUnit,Beat,Measure


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


#### Beat ####

def test_Beat_constructor_given_subdivision():
    b = Beat(4)

    assert b.subdivision == 4
    assert type(b.time_units) == np.ndarray
    assert b.time_units.ndim == 1

    # all TimeUnit instances have `state` == 0
    assert set([tu.state for tu in b.time_units]).issubset({0})

    with pytest.raises(TypeError):
        Beat("1")
    with pytest.raises(ValueError):
        invalid = [0, -1]
        [Beat(a) for a in invalid]

def test_Beat_constructor_given_iterable():
    b = Beat([1, 0, 1, 2])

    assert b.subdivision == 4
    assert type(b.time_units) == np.ndarray
    assert b.time_units.ndim == 1
    assert b[0].state == 1
    assert b[-1].state == 2

    b = Beat([TimeUnit(0), 1, 2])

    assert b.subdivision == 3
    assert type(b.time_units) == np.ndarray
    assert b.time_units.ndim == 1

    with pytest.raises(TypeError):
        invalid = [
            "1012",
            [1, 0, "1", 2]
        ]
        [Beat(a) for a in invalid]

    with pytest.raises(ValueError):
        invalid = [
            [1,2,3],
            [0,-1]
        ]
        [Beat(a) for a in invalid]

def test_Beat_iterator():
    b = Beat(4)

    for tu in b:
        assert type(tu) == TimeUnit

def test_Beat_indexing():
    b = Beat([0,1,2,0])
    assert type(b[0]) == TimeUnit
    assert b[3].state == 0

def test_Beat_mul():

    b = Beat([1,2,0])
    beats = b * 2

    for b_copy in beats:
        assert b_copy.subdivision == 3
        assert type(b_copy[0]) == TimeUnit
        assert b_copy[0].state == 1


#### Measure ####

def test_Measure_constructor():

    # given Beat instances
    beats = [Beat(4),Beat([1,1,1])]
    m = Measure(beats=beats)
    assert type(m.beats) == np.ndarray
    assert m.n_beats == 2
    assert m.beats[0].subdivision == 4
    assert m.beats[0][0].state == 0
    assert m.beats[1].subdivision == 3
    assert m.beats[1][0].state == 1

    # given integers
    beats = [4, 4, 3]
    m = Measure(beats=beats)
    assert type(m.beats) == np.ndarray
    assert m.n_beats == 3
    assert m.beats[0].subdivision == 4
    assert m.beats[0][0].state == 0
    assert m.beats[1].subdivision == 4

    # given mixture
    beats = (
        4,Beat(4),Beat([1,0,1,2]),5
    )







def test_Measure_constructor_given_mixture():

    # beats = (4,Beat,5)
    # Measure(beats)
    pass

# TODO
def test_Measure_constructor_fails():
    pass


def test_Measure_iterator():
    measure = Measure(beats=[
        Beat(3),
        Beat([1,1,0]),
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
    assert measure[1].time_units[0].state == 1
    assert measure[1].time_units[-1].state == 0

    assert measure[2].subdivision == 4
