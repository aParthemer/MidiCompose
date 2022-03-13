import pytest

from MidiCompose.logic.harmony.note import Note
from MidiCompose.logic.harmony.interval import Interval

def test_constructor_hs():

    interval = Interval(0)
    assert interval.hs == 0
    assert interval.string == "P1"

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

    interval = Interval("P1")
    assert interval.string == "P1"
    assert interval.hs == 0
    assert interval.quality == "P"
    assert interval.value == 1
    assert interval.octave_shift == 0


    with pytest.raises(ValueError):
        invalid_strings = ["A","Bb","U-","P5-"]
        [Interval(s) for s in invalid_strings]

def test_above_and_below():
    """
    Supports comparison between integers AND key Note objects.
    """

    # pass an integer
    note = 60
    assert Interval("M3").above(note) == 64 == Note(64)
    assert type(Interval("M3").above(note)) == Note
    assert Interval("M3").below(note) == 56 == Note(56)

    # pass Note object
    note = Note(60)
    assert Interval("P4").above(note) == 65 == Note(65)
    assert type(Interval("P4").above(note)) == Note
    assert Interval("P4").below(note) == 55 == Note(55)
    # assert Interval("P4").steps_below(item)

def test_from_get_staticmethod():

    i = Interval.get(quality="M",value=3)
    assert i == Interval("M3")
