import pytest
from icecream import ic
from mido import Message

from MidiCompose.logic.harmony.note import Note
from MidiCompose.logic.rhythm.beat import Beat
from MidiCompose.logic.rhythm.measure import Measure
from MidiCompose.translation import midi_translation as mt
from tests.test_translation import TEST_CONSTANTS as TC



