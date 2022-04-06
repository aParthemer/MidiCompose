import pytest
from icecream import ic
from mido import Message

from compositional.logic.harmony.note import Note
from compositional.logic.rhythm.beat import Beat
from compositional.logic.rhythm.measure import Measure
from compositional.translation import midi_translation as mt
from tests.test_translation import TEST_CONSTANTS as TC


#### MESSAGE PROTOCOLS ###
@pytest.mark.parametrize(
    ["constructor_kwargs","expected"],
    [
        (TC.ofn_kwargs_1,TC.ofn_expected_1)
    ]
)
def test_ofn(kwargs,expected):
    messages = mt.ofn(**kwargs)
    off_msg,on_msg = messages[0],messages[1]

    assert len(messages) == expected.n_messages
    assert set([type(m) for m in messages]) == {Message}

    assert off_msg.type == expected.off_type
    assert off_msg.time == expected.off_timedelta
    assert off_msg.note == expected.off_note
    assert off_msg.channel == expected.off_channel

    assert on_msg.type == expected.on_type
    assert on_msg.time == expected.on_timedelta
    assert on_msg.note == expected.on_note
    assert on_msg.velocity == expected.on_velocity
    assert on_msg.channel == expected.on_channel



