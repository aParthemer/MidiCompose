import collections
from typing import Optional

import numpy as np
import pytest

from compositional.logic.harmony.note import Note
from compositional.logic.melody.melody import Melody

from tests.test_objects import melody_obj as mo


@pytest.mark.parametrize(
    "notes",
    [
        [Note(60), Note(64)],
        None,
        [Note(60), 64],
        [60, 64]
    ]
)
def test_constructor(notes):
    melody = Melody(notes)

    assert isinstance(melody.notes, list)
    assert set([type(n) for n in melody.notes]).issubset({Note})

    # default velocity
    assert melody.velocity.size == len(melody)
    assert np.all(melody.velocity == 64)

@pytest.mark.parametrize(
    ["melodies","velocity","error"],
    [
        (mo.mel_60_62_64,[50,55,60],None),  # list of ints
        (mo.mel_60_62_64,np.array([50,55,60]),None),  # array of ints
        (mo.mel_60_62_64,70,None),  # single int
        (mo.mel_60_62_64,[60,60],ValueError)  # invalid size
    ]
)
def test_velocity_setter(melodies, velocity, error):

    if error is not None:
        with pytest.raises(error):
            melodies.velocity = velocity

    else:
        melodies.velocity = velocity

        assert isinstance(melodies.velocity, np.ndarray)
        assert melodies.velocity.size == len(melodies)

        if isinstance(velocity,collections.Sequence):  # doesn't apply to single integers
            assert set(melodies.velocity) == set(velocity)


    pass

def test_iterator():
    pass

