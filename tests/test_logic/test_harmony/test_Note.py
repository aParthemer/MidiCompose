import pytest

from MidiCompose.logic.harmony.note import Note


#### INITIALIZATION ####


@pytest.mark.parametrize(
    ["note", "expected_value"],
    [
        (60, 60),
        ("C3", 60),
        ("D#6", 99),
        ("Db-1",13)
    ]
)
def test_constructor(note, expected_value):

    n = Note(note=note)

    assert n.value == expected_value



#### UTILITY METHODS ####


@pytest.mark.parametrize(
    ["note","accidental","expected"],
    [
        (Note(60),None,"C3"),
        (Note("Db4"),"sharp","C#4"),
        (Note("F#6"),None,"Gb6")
    ]
)
def test_as_letter(note,accidental,expected):

    assert note.as_letter(accidental) == expected


#### SPECIAL METHODS ####


@pytest.mark.parametrize(
    ["note","equivalent"],
    [
        (Note(60),60),
        (Note(65),Note(65)),
        (Note("C0"),24),
        (Note("C#0"),Note(25))
    ]
)
def test_eq(note,equivalent):
    assert note == equivalent


@pytest.mark.parametrize(
    ["note","comparison","less","greater"],
    [
        (Note(60),Note(59),False,True),
        (Note(60),61,True,False),
        (Note(60),60,False,False)
    ]
)
def test_lt_gt(note,comparison,less,greater):

    assert (note < comparison) is less
    assert (note > comparison) is greater


@pytest.mark.parametrize(
    ["note","comparison","less_or_equal","greater_or_equal"],
    [
        (Note(60),60,True,True),
        (Note(60),61,True,False),
        (Note(60),Note(59),False,True)
    ]
)
def test_le_ge(note,comparison,less_or_equal,greater_or_equal):

    assert (note <= comparison) is less_or_equal
    assert (note >= comparison) is greater_or_equal


