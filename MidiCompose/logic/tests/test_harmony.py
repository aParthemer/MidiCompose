import pytest

from MidiCompose.logic.harmony import Interval

#### NOTE ####


#### INTERVAL ####

# constructor takes half steps
def test_constructor_hs():
    interval = Interval(3)
    assert interval.hs == 3
    assert interval.string == "m3"

    interval = Interval(16)
    assert interval.hs == 16
    assert interval.string == "M3+"

    interval = Interval(27)
    assert interval.string == "m3++"
    assert interval.hs == 27
    assert interval.quality == "m"
    assert interval.value == 3
    assert interval.octave_shift == 2

    with pytest.raises(ValueError):
        out_of_range = [-1,128]
        for n in out_of_range:
            interval = Interval(n)

# constructor takes string representation
def test_constructor_string():

    interval = Interval("P4")
    assert interval.string == "P4"
    assert interval.hs == 5
    assert interval.quality == "P"
    assert interval.value == 4
    assert interval.octave_shift == 0

    interval = Interval("m3++")
    assert interval.string == "m3++"
    assert interval.hs == 27
    assert interval.quality == "m"
    assert interval.value == 3
    assert interval.octave_shift == 2

    with pytest.raises(ValueError):
        invalid_strings = ["A","Bb","U-","P5-"]
        [Interval(s) for s in invalid_strings]

def test_above():
    note = 60
    assert Interval("M3").above(note) == 64

def test_below():
    note = 60
    assert Interval("M3").below(note) == 56
