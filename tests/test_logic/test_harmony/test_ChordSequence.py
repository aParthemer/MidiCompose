import pytest

from MidiCompose.objects import Note,Chord,ChordSequence

def test_constructor():
    valid = [
        Chord([Note(60),Note(64),Note(67)]),
        Chord.from_figured_bass(figured_bass=(Note("C3"),[4,5,6]))
    ]

    cs = ChordSequence(chords=valid)

    assert len(cs) == 2
    assert cs[0].notes == [Note(60),Note(64),Note(67)]
    assert cs.max_notes == 4
    assert all([isinstance(c,Chord) for c in cs])

def test_constructor_fails():

    invalid_chords = [
        Chord([Note(34), Note(35)]),
        [36, 38]
    ]
    with pytest.raises(TypeError):
        cs = ChordSequence(chords=invalid_chords)


