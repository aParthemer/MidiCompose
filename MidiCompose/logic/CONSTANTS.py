from collections import namedtuple
from dataclasses import dataclass

from pydantic import BaseModel
from icecream import ic


# midi range objects
class MidiRange(BaseModel):
    piano: set = set(range(21, 109))
    absolute: set = set(range(0, 128))


####                    ####
#### HARMONIC CONSTANTS ####
####                    ####

# ordinal pitch sets #

IONIAN = [0, 2, 4, 5, 7, 9, 11]
DORIAN = [0, 2, 3, 5, 7, 9, 10]
PHRYGIAN = [0, 1, 3, 5, 7, 8, 10]
LYDIAN = [0, 2, 4, 6, 7, 9, 11]
MIXOLYDIAN = [0, 2, 4, 5, 7, 9, 10]
AEOLIAN = [0, 2, 3, 5, 7, 8, 10]
LOCRIAN = [0, 1, 3, 5, 6, 8, 10]

DIATONIC_MODES = [IONIAN, DORIAN, PHRYGIAN, LYDIAN,
                  MIXOLYDIAN, AEOLIAN, LOCRIAN]

####                      ####
#### MAPPING DICTIONARIES ####
####                      ####

PIANO_MIDI_RANGE = list(range(21, 109))

LETTER_ORD_DICT = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11
}

HS_INTERVAL_DICT = {
    0: 'U',
    1: 'm2',
    2: 'M2',
    3: 'm3',
    4: 'M3',
    5: 'P4',
    6: 'A4',
    7: 'P5',
    8: 'm6',
    9: 'M6',
    10: 'm7',
    11: 'M7',
}

#### INTERVAL MAPPER (TwoWayDict) ####
def _populate_interval_mapper():
    class TwoWayDict(dict):
        def __setitem__(self, key, value):
            # Remove any previous connections with these values
            if key in self:
                del self[key]
            if value in self:
                del self[value]
            dict.__setitem__(self, key, value)
            dict.__setitem__(self, value, key)

        def __delitem__(self, key):
            dict.__delitem__(self, self[key])
            dict.__delitem__(self, key)

        def __len__(self):
            """Returns the number of connections"""
            return dict.__len__(self) // 2

    interval_mapper = TwoWayDict()
    for _hs in range(0, 127):
        oct_shift, hs = divmod(_hs, 12)
        oct_shift = int(oct_shift)

        qual_val = HS_INTERVAL_DICT[hs]

        interval = qual_val + str(oct_shift * "+")
        interval_mapper[_hs] = interval

    return interval_mapper


INTERVAL_MAPPER = _populate_interval_mapper()
