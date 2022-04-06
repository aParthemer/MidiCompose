import pytest

from compositional.logic.harmony.key import Key, KeySchema
from compositional.logic.harmony.note import Note

import itertools

@pytest.fixture
def C_MAJOR():
    return Key("C MAJOR")

# CONSTRUCTOR #
@pytest.mark.parametrize(
    argnames=["args", "expected"],
    argvalues=[
        (
                ["C"],
                {"tonic": Note("C-2"), "notes": [Note(Note(n).signature) for n in "CDEFGAB"]}
        ),
        (
                {"tonic": Note("Gb"), "key_schema": "HARMONIC_MINOR"},
                {"tonic": Note("Gb"), "notes": [Note(Note(n).signature)
                                                for n in "Gb,Ab,A,B,Db,D,F".split(",")]}
        )
    ]
)
def test_constructor(args, expected):
    if isinstance(args, list):
        key = Key(*args)
    else:
        key = Key(**args)

    for k, v in expected.items():
        assert getattr(key, k) == v

@pytest.mark.parametrize(
    ["key","depth","expected_keys","error"],
    [
        (Key("C MAJOR"), 1, [Key(t + " MAJOR") for t in "F,G".split(",")], None),
        (Key("D MIXOLYDIAN"),2,[Key(t + " MIXOLYDIAN") for t in "A,E,G,C".split(",")],None),
        (Key("F MAJOR"),7,None,ValueError)
    ]
)
def test_get_neighbors(key,depth,expected_keys,error):
    if error is not None:
        with pytest.raises(error):
            neighbors = key.get_neighbors(depth)

    neighbors = key.get_neighbors(depth)
    neighbors_flattened = list(itertools.chain.from_iterable(neighbors))

    assert all([k in neighbors_flattened for k in expected_keys])

def test_get_index_of(C_MAJOR):

    assert C_MAJOR.get_index_of("C") == 0
    assert C_MAJOR.get_index_of("G3") == 4

    with pytest.raises(Exception):
        C_MAJOR.get_index_of("Db")

def test_next_note(C_MAJOR):
    assert C_MAJOR.next_note(from_note="D") == Note("E").signature
    assert C_MAJOR.next_note(from_note="A",step=3) == Note("D").signature

    with pytest.raises(Exception):
        C_MAJOR.next_note("Ab")

def test_previous_note():
    key = Key("D HARMONIC_MINOR")

    assert key.previous_note("D") == Note("C#")
    assert key.previous_note("A",step=2) == Note("F")

    with pytest.raises(Exception):
        key.previous_note("Eb")

def test_note_range():
    key = Key("F Lydian")

    _range = key.note_range(a="F2",b="C3")
    assert _range == [Note(n) for n in "F2,G2,A2,B2,C3".split(",")]

    _range_reversed = key.note_range(a="C3",b="F2")
    assert _range_reversed == [Note(n) for n in "C3,B2,A2,G2,F2".split(",")]

# STATIC METHODS #
@pytest.mark.parametrize(
    ["kwargs","expected"],
    [
        (
            {"notes":[Note(n) for n in "C,D,Eb".split(",")]},
            [Key(t + " MAJOR") for t in "Eb,Bb".split(",")]
        ),
        (
            {"notes":Note("D"),"key_schemas":[KeySchema.parse(v) for v in ("MAJOR","MINOR")]},
            [Key(t + " major") for t in "d,eb,f,g,a,bb,c".split(",")] +
            [Key(t + " minor") for t in "d,e,gb,g,a,b,c".split(",")]
        )
    ]

)
def test_all_keys_with(kwargs,expected):
    keys_with = Key.all_keys_with(**kwargs)

    assert all([k in expected for k in keys_with])
    assert all([k in keys_with for k in expected])

