import pytest
from itertools import groupby

from compositional.logic.harmony.figure import AbstractBaseFiguredNote, TonalFiguredNote, BaseFiguredNote, ChromaticFiguredNote
from compositional.logic.harmony.interval import Interval
from compositional.logic.harmony.key import Key
from compositional.logic.harmony.note import Note

@pytest.mark.parametrize(
    argnames="kwargs",
    argvalues=[
        {
            "constructor":{"from_note":"C3","figure":(5,3,3),"index":0},
            "validation":{"from_note":Note("C3"),"figure":[0,3,5],"index":0},
        },
        {
            "constructor":{"from_note":"C3","figure":[0,5,10],"index":3},
            "error":ValueError
        }
    ]
)
def test_BaseFiguredNote(kwargs):
    constructor = kwargs["constructor"]
    validation = kwargs.get("validation")
    error = kwargs.get("error")

    if error is not None:
        with pytest.raises(error):
            bf = BaseFiguredNote(**constructor)
    else:
        bf = BaseFiguredNote(**constructor)
        for k,v in validation.items():
            assert getattr(bf,k) == v

@pytest.mark.parametrize(
    argnames="kwargs",
    argvalues=[
        {
            "constructor":{"from_note":"C3","figure":(5,3,3),"index":0},
            "validation":{"from_note":Note("C3"),"figure":[0,3,5],"index":0,
                          "bass":Note("C3"),"notes":[Note(n) for n in (60,63,65)]},
        },
        {
            "constructor":{"from_note":60,"figure":[0,5,9],"index":3},
            "error":ValueError
        }
    ]

)
def test_ChromaticFiguredNote(kwargs):
    constructor = kwargs["constructor"]
    error = kwargs.get("error")
    validation = kwargs.get("validation")

    if error is not None:
        with pytest.raises(error):
            cf = ChromaticFiguredNote(**constructor)
    else:
        cf = ChromaticFiguredNote(**constructor)
        for k,v in validation.items():
            assert getattr(cf,k) == v

@pytest.mark.parametrize(
    argnames="kwargs",
    argvalues=[
        {
            "constructor":{"from_note":"C3","figure":(5,3,3),"index":1,"key":"C"},
            "validation":{"from_note":Note("C3"),"figure":[0,3,5],"index":1,
                          "bass":Note("A2"),"notes":[Note(n) for n in ("A2","C3","E3")]},
        },
        {
            "constructor":{"from_note":"C3","figure":[0,5,9],"index":0,"key":"D"},
            "error":ValueError
        }
    ]
)
def test_TonalFiguredNote(kwargs):

    constructor = kwargs["constructor"]
    error = kwargs.get("error")
    validation = kwargs.get("validation")

    if error is not None:
        with pytest.raises(error):
            tf = TonalFiguredNote(**constructor)

    else:
        tf = TonalFiguredNote(**constructor)
        for k,v in validation.items():
            assert getattr(tf,k) == v

