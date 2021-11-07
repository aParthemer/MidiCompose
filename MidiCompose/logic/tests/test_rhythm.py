from typing import List

import pytest

import numpy as np
from numpy.testing import assert_array_equal
from icecream import ic

from MidiCompose.logic.rhythm import TimeUnit, Beat, Measure
from MidiCompose.logic.tests import TEST_CONSTANTS as TC


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


