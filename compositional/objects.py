from typing import List, Optional
from importlib import import_module

from compositional.logic.harmony.note import Note,HasNotes
from compositional.logic.harmony.chord import Chord
from compositional.logic.harmony.chord_sequence import ChordSequence
from compositional.logic.harmony.interval import Interval
from compositional.logic.harmony.interval import IntervalRange
from compositional.logic.harmony.key import Key
from compositional.logic.harmony.figure import TonalFiguredNote, ChromaticFiguredNote

from compositional.logic.melody.melody import Melody
from compositional.logic.melody.note_set import NoteSet
from compositional.logic.melody.scale import Scale, DiatonicModes, NonDiatonicModes, AllModes

from compositional.logic.rhythm.time_unit import TimeUnit
from compositional.logic.rhythm.beat import Beat
from compositional.logic.rhythm.measure import Measure
from compositional.logic.rhythm.part import Part

from compositional.translation.track_builder import TrackBuilder

from compositional.playback import play_mid

from compositional.utilities import ctx_random_seed

