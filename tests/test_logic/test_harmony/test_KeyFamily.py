import pytest

from MidiCompose.logic.harmony.key import KeyFamily
from MidiCompose.logic.harmony.note import Note

FAM_C = [Note(n) for n in [0, 2, 4, 5, 7, 9, 11]]
FAM_D = [Note(n) for n in [2, 4, 6, 7, 9, 11, 1]]
FAM_Gb = [Note(n) for n in [6, 8, 10, 11, 1, 3, 5]]


@pytest.mark.parametrize(
    ["arg_family", "expected_notes"],
    [
        ("C", FAM_C),  # non-ranged note string
        (Note("C"), FAM_C),  # note object
        (Note("Gb"), FAM_Gb),
        ("D4", FAM_D),  # ranged note string
        (62, FAM_D)
    ]
)
def test_constructor(arg_family, expected_notes):
    key_fam = KeyFamily(family=arg_family)

    assert key_fam.notes == expected_notes


@pytest.mark.parametrize(
    ["arg", "expected"],
    [
        (Note("C"), True),
        (Note("C#"), False),
        ("C", True),
        ("G4", True),
        (60, True),
        (61, False)
    ]
)
def test_contains(arg, expected):
    kf = KeyFamily("C")
    result = (arg in kf)

    assert expected == result


#### STATIC METHODS ####

@pytest.mark.parametrize(
    ["notes", "expected"],
    [
        (Note("C"), [KeyFamily(n) for n in ["C", "Db", "Eb", "F", "G", "Ab", "Bb"]]),
        (["C", "Db", "D"], [])  # no keys contain 3 half-steps
    ]
)
def test_keys_with(notes, expected):
    keys = KeyFamily.all_keys_with(notes)

    key_sigs = [kf.family.signature for kf in keys]
    expected_sigs = [kf.family.signature for kf in expected]

    assert set(key_sigs) == set(expected_sigs)
