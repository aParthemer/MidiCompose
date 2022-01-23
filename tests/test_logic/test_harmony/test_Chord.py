import pytest

from MidiCompose.objects import Chord,Note

@pytest.mark.parametrize(
    ["notes","expected_notes","error"],
    [
        ([Note("C3"), Note("E3"), Note("G3")],
         [Note("C3"), Note("E3"), Note("G3")],
         None),
        # reorders notes
        ([Note("C3"), Note("G3"), Note("E3")],
         [Note("C3"), Note("E3"), Note("G3")],
         None),
        # enforces uniqueness
        ([Note(60),Note(64),Note(64),Note(67)],
         [Note(60),Note(64),Note(67)],
         None),
        # handles sequence of ints
        ([60,64,67],
         [Note(60),Note(64),Note(67)],
         None),
        # handles no notes arg
        (None,[],None),
        # raises error given single Note
        ([Note(60)],None,ValueError),
        # raises error, item out of range
        ([60,128],None,ValueError)
    ]
)
def test_constructor(notes,expected_notes,error):

    if error:
        with pytest.raises(error):
            c = Chord(notes=notes)
    else:
        c = Chord(notes=notes)

        assert c.notes == expected_notes
        assert len(set(c.notes)) == len(c.notes)  # all unique

def test_from_figured_bass():
    pass

def test_invert():
    pass

def test_equality():
    pass

