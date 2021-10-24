import pytest

from MidiCompose.logic.harmony import Note,Interval

#### NOTE ####
def test_note_constructor():

    n = Note(60)
    assert n.value == 60

    notes_invalid_type = [1.1]
    with pytest.raises(TypeError):
        [Note(n) for n in notes_invalid_type]

    # notes_out_of_range = [-1,128]
    with pytest.raises(ValueError):
        Note(-1)

#### INTERVAL ####


def test_Interval_constructor_hs():
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

def test_Interval_constructor_string():

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

def test_Interval_above_and_below():
    """
    Supports comparison between integers AND other Note objects.
    """

    # pass an integer
    note = 60
    assert Interval("M3").above(note) == 64
    assert Interval("M3").above(note) == Note(64)
    assert Interval("M3").below(note) == 56
    assert Interval("M3").below(note) == Note(56)

    # pass Note object
    note = Note(60)
    assert Interval("P4").above(note) == 65
    assert Interval("P4").above(note) == Note(65)
    assert Interval("P4").below(note) == 55
    assert Interval("P4").below(note) == Note(55)

