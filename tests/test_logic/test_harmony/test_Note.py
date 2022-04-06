import pytest

from compositional.logic.harmony.note import Note


#### INITIALIZATION ####
@pytest.mark.parametrize(
    ["item", "expected_value"],
    [
        (60, 60),
        ("C3", 60),
        ("D#6", 99),
        ("Db-1",13),
        ("C",0)
    ])
def test_constructor(item, expected_value):

    n = Note(note=item)

    assert n.value == expected_value



#### UTILITY METHODS ####


@pytest.mark.parametrize(
    ["item","accidental","expected"],
    [
        (Note(60),None,"C3"),
        (Note("Db4"),"sharp","C#4"),
        (Note("F#6"),None,"Gb6")
    ]
)
def test_as_letter(item,accidental,expected):

    assert item.as_letter(accidental) == expected


#### SPECIAL METHODS ####


@pytest.mark.parametrize(
    ["item","equivalent"],
    [
        (Note(60),60),
        (Note(65),Note(65)),
        (Note("C0"),24),
        (Note("C#0"),Note(25))
    ]
)
def test_eq(item, equivalent):
    assert item == equivalent


@pytest.mark.parametrize(
    ["item","comparison","less","greater"],
    [
        (Note(60),Note(59),False,True),
        (Note(60),61,True,False),
        (Note(60),60,False,False)
    ]
)
def test_lt_gt(item, comparison, less, greater):

    assert (item < comparison) is less
    assert (item > comparison) is greater


@pytest.mark.parametrize(
    ["item","comparison","less_or_equal","greater_or_equal"],
    [
        (Note(60),60,True,True),
        (Note(60),61,True,False),
        (Note(60),Note(59),False,True)
    ]
)
def test_le_ge(item, comparison, less_or_equal, greater_or_equal):

    assert (item <= comparison) is less_or_equal
    assert (item >= comparison) is greater_or_equal


