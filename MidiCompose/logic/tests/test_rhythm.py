from typing import List

import pytest

import numpy as np
from icecream import ic

from MidiCompose.logic import rhythm as r


#### TimeUnit ####

def test_TimeUnit_constructor():
    tu = r.TimeUnit()
    assert tu.state == 0

    tu.activate()
    assert tu.state == 1

    tu.sustain()
    assert tu.state == 2

    tu.deactivate()
    assert tu.state == 0

    with pytest.raises(TypeError):
        invalid = ["1", 1.1]

        [r.TimeUnit(a) for a in invalid]

    with pytest.raises(ValueError):
        invalid = [-1, 3]
        [r.TimeUnit(a) for a in invalid]


#### Beat ####

def test_Beat_constructor_given_subdivision():
    b = r.Beat(4)

    assert b.subdivision == 4
    assert type(b.time_units) == np.ndarray
    assert b.time_units.ndim == 1

    time_units = list(b.time_units)
    for tu in time_units:
        assert type(tu) == r.TimeUnit
        assert tu.state == 0

    with pytest.raises(TypeError):
        b = r.Beat("1")
    with pytest.raises(ValueError):
        invalid = [0, -1]
        [r.Beat(a) for a in invalid]


def test_Beat_constructor_given_iterable():
    b = r.Beat([1, 0, 1, 2])

    assert b.subdivision == 4
    assert type(b.time_units) == np.ndarray
    assert b.time_units.ndim == 1

    b = r.Beat([r.TimeUnit(0), 1, 2])

    assert b.subdivision == 3
    assert type(b.time_units) == np.ndarray
    assert b.time_units.ndim == 1

    with pytest.raises(TypeError):
        invalid = [
            "1012",
            [1, 0, "1", 2]
        ]
        [r.Beat(a) for a in invalid]

    with pytest.raises(ValueError):
        invalid = [
            [1,2,3],
            [0,-1]
        ]
        [r.Beat(a) for a in invalid]

def test_Beat_iterator():
    b = r.Beat(4)

    for tu in b:
        assert type(tu) == r.TimeUnit

def test_Beat_indexing():
    b = r.Beat([0,1,2,0])
    assert type(b[0]) == r.TimeUnit
    assert b[3].state == 0

def test_Beat_mul():

    b = r.Beat([1,2,0])
    beats = b * 2

    for b_copy in beats:
        assert b_copy.subdivision == 3
        assert type(b_copy[0]) == r.TimeUnit
        assert b_copy[0].state == 1


#### Measure ####

def test_Measure_constructor_given_nbeats_and_subdivision():
    kwargs = {
        "n_beats":4,
        "subdivision":4
    }

    m = r.Measure(**kwargs)
    assert m.n_beats == 4
    assert type(m.beats) == np.ndarray
    assert m.beats.size == 4


def test_Measure_constructor_given_Beats():
    beats = [r.Beat(4),r.Beat([1,1,1])]
    m = r.Measure(beats=beats)
    assert m.n_beats == 2

    assert m.beats[0].subdivision == 4
    assert m.beats[0][0].state == 0

    assert m.beats[1].subdivision == 3
    assert m.beats[1][0].state == 1


def test_Measure_constructor_fails():

    attribute_kwargs = [
        {"n_beats": 4, "subdivision": 4, "beats": r.Beat() * 4},
        {"n_beats": 4, "beats": r.Beat() * 4},
    ]
    b = r.Beat([1,2,0,1])
    for k in attribute_kwargs:
        with pytest.raises(AttributeError):
            r.Measure(**k)

    type_kwargs = [
        {"n_beats":4,"subdivision":"4"},
        {"beats":[1,2,3]}
    ]
    for k in type_kwargs:
        with pytest.raises(TypeError):
            r.Measure(**k)


def test_Measure_iterator():
    measure = r.Measure(beats=[
        r.Beat(3),
        r.Beat([1,1,0]),
        r.Beat(4)
    ])
    for beat in measure:
        assert type(beat) == r.Beat

def test_Measure_indexing():
    measure = r.Measure(beats=[
        r.Beat(3),
        r.Beat([1, 1, 0]),
        r.Beat(4)
    ])
    assert measure[0].subdivision == 3

    assert measure[1].subdivision == 3
    assert measure[1].time_units[0].state == 1
    assert measure[1].time_units[-1].state == 0

    assert measure[2].subdivision == 4
