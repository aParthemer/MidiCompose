from dataclasses import dataclass, asdict
from typing import Optional

import numpy as np
import pytest
from icecream import ic

from MidiCompose.logic.rhythm.measure import Measure
from MidiCompose.logic.rhythm.beat import Beat
from MidiCompose.logic.rhythm.part import Part

from MidiCompose.logic.harmony.note import Note

from MidiCompose.logic.melody.note_set import NoteSet
from MidiCompose.logic.melody import scale


@dataclass
class OfnKwargs:
    timedelta: int
    off_note: int
    on_note: int
    channel: int = 0
    velocity: int = 64


@dataclass
class OfnExpected:
    n_messages: int

    off_timedelta: int
    off_note: int

    on_timedelta: int
    on_note: int
    on_velocity: int

    off_channel: int = 0
    off_type: str = "note_off"
    on_channel: int = 0
    on_type: str = "note_on"


ofn_kwargs_1 = asdict(OfnKwargs(timedelta=50, off_note=60, on_note=64))
ofn_expected_1 = OfnExpected(n_messages=2, off_timedelta=50, off_note=60, off_channel=0,
                             on_timedelta=0, on_note=64, on_velocity=64)

#### NOTESET OBJECTS ####
noteset_c_major = NoteSet().from_scale(tonic=Note("C3"),
                                       scale=scale.DiatonicModes.MAJOR, )
ic(noteset_c_major)

#### MEASURE/MELODY PAIRS ####
measure_ends_0 = Measure([Beat([1, 2, 1, 0]),
                          Beat([1, 1, 1, 0])])
melody_meas_ends_0 = noteset_c_major.random_sample(n=measure_ends_0.n_note_on,
                                                   _cycle=True, random_seed=0)

measure_starts_2 = Measure([Beat([2, 2, 1, 1]),
                            Beat([1, 0, 1, 2])])
melody_meas_starts_2 = noteset_c_major.random_sample(n=measure_starts_2.n_note_on,
                                                     _cycle=True, random_seed=0)
