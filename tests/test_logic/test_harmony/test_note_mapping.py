import pytest

from MidiCompose.logic.harmony import note_mapping as nm


@pytest.mark.parametrize(
    ["note_value", "accidental","raises","expected"],
    [
        (0,None,False,"C-2"),
        (1,"flat",False,"Db-2"),
        (1, "sharp",False,"C#-2"),
        (60,None,False,"C3"),
        (128,None,True,ValueError)

    ]
)
def test_value_to_letter(note_value, accidental, raises, expected):
    if raises:
        with pytest.raises(expected):
            nm.value_to_letter(value=note_value,accidental=accidental)
    else:
        assert nm.value_to_letter(note_value,accidental) == expected


@pytest.mark.parametrize(
    ["note_letter","raises","expected"],
    [
        ("C-2",False,0),
        ("F#8",False,126),
        ("Gb8",False,126),
        ("G8",False,127)
    ]
)
def test_letter_to_value(note_letter,raises,expected):
    if raises:
        with pytest.raises(expected):
            nm.letter_to_value(letter=note_letter)
    else:
        assert nm.letter_to_value(letter=note_letter) == expected


