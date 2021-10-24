from collections import namedtuple
from dataclasses import dataclass

"""
Midi-range: (C-2,G8) : (0,127)
Piano-range: (A0,C8) : (21,
"""

# TODO
####
string_to_midi = namedtuple("StringToMidi",
                            ["string_note","midi_note"])
@dataclass
class StringNoteMidiMapper:
    """
    Maps string representation of a note to its midi value.

    - register-aware:
        - Note-string followed by octave number.
        - Octave numbers based on piano octave range convention

    """
    note_str: str
    note_val: int
####


# TODO : get ranges in terms of Note objects rather than bare integers
@dataclass
class InstrumentRange:
    """
    Contains the midi-value range of various instruments.
    """
    piano = range(21,108)


