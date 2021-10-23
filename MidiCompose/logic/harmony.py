"""
Interval as purely descriptive. Not tied to absolute notes, values but must be derived
from two notes.

Represents the distance (non-directional) between two notes.

Requirements:
    - Always assumes ascending (no such thing as "M3 below", for example)
    - To initialize, must be given either:
        - hs
        - quality AND value (AND octave_shift if applicable)
"""
from dataclasses import dataclass
from typing import Optional, Union, Literal

from icecream import ic

import CONSTANTS as C


# TODO: include translator for string representation (register and non-register)
# TODO: include optional `tonality` parameter to inform string representations based on key (Bb vs A#)
# TODO: implement _update_attributes() for when and attribute is set manually or by operation
class Note:
    """
    Used mostly for validation and translating between note representation in other classes.
    """

    def __init__(self, note: int, verbose: bool = False):

        # valid representations
        self.value: Optional[int] = None
        self.letter_oct: Optional[str] = None

        self.letter: Optional[str] = None

        self.verbose = verbose
        self._parse_input(note)

    def _parse_input(self, note):
        if not isinstance(note, int):
            msg = "Midi-value notes must be an integer."
            raise TypeError(msg)

        elif note not in range(128):
            msg = "Midi-value notes must be an integer between 0-127"
            raise ValueError(msg)

        self.value = note

    #### SPECIAL METHODS ####
    def __eq__(self, other):
        if self.value == other.value:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.value < other.value:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.value > other.value:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.value != other.value:
            return True
        else:
            return False

    def __add__(self, other):
        value = self.value + other.value
        try:
            new_note = Note(value)
        except:
            msg = f"The value `{value}` produced by the operation resulted in an invalid midi-value."
            raise ValueError(msg)

    def __sub__(self, other):
        value = self.value - other.value
        try:
            new_note = Note(value)
        except:
            msg = f"The value `{value}` produced by the operation resulted in an invalid midi-value."
            raise ValueError(msg)

    def __repr__(self):
        if self.verbose:
            r = "set up verbose repr!!"
            pass
        else:
            r = f"MidiNote({self.value})"

        return r

class Interval:
    """
    Constructor takes only one required argument:
        - number of half steps (int) -- 16
        OR
        - string representation -- "M3+"
    """

    def __init__(self, interval: Union[int, str], verbose: bool = True):

        # full representations
        self.hs: Optional[int] = None
        self.string: Optional[str] = None

        # individual attributes
        self.quality: Optional[str] = None
        self.value: Optional[int] = None
        self.octave_shift: Optional[int] = None

        # verbosity of __repr__
        self.verbose: bool = verbose

        self._parse_interval_arg(interval)

    def _parse_interval_arg(self, interval: Union[int, str]):

        if isinstance(interval, int):
            if interval not in range(0, 128):
                msg = f"Interval `{interval}` out of range."
                raise ValueError(msg)

            self.hs = interval
            self.string = C.INTERVAL_MAPPER[self.hs]

        elif isinstance(interval, str):
            try:
                self.string = interval
                self.hs = C.INTERVAL_MAPPER[interval]
            except:
                msg = f"Interval `{interval}` is an invalid string representation."
                raise ValueError(msg)

        else:
            msg = "Parameter `interval` must be given either an integer of half-steps, or a" \
                  "string representation of an interval."
            raise TypeError(msg)

        # set individual attributes
        self.quality = self.string[0]
        self.value = int(self.string[1])
        self.octave_shift = len(self.string[2:])

    #### SPECIAL METHODS ####
    def __eq__(self, other):
        if self.hs == other.hs:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.hs < other.hs:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.hs > other.hs:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.hs > other.hs:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.hs != other.hs:
            return True
        else:
            return False

    def __repr__(self):
        if self.verbose:
            header = "Interval("
            string_rep = f'string = "{self.string}", '
            quality = f'quality = "{str(self.quality)}", '
            value = f"value = {str(self.value)}, "
            octave_shift = f"octave_shift = {str(self.octave_shift)}, "
            hs = f"hs = {str(self.hs)}"
            footer = ")"

            r = header + string_rep + quality + value + octave_shift + hs + footer

            return r

        else:
            r = f'"{self.string}"'
            return r

    #### UTILITY METHODS ####
    def above(self, note: Union[Note, int, str]) -> Note:
        """
        Given a valid note representation, return the note above said note.
        :param note:
        :return: MidiNote
        """
        # coerce to MidiNote object
        if not isinstance(note, Note):
            try:
                note = Note(note)
            except:
                msg = f"`{note}` is an invalid argument."
                raise ValueError(msg)

        result_value = note.value + self.hs

        return Note(result_value)

    def below(self, note:Union[Note, int, str]) -> Note:

        # coerce to MidiNote object
        if not isinstance(note, Note):
            try:
                note = Note(note)
            except:
                msg = f"`{note}` is an invalid argument."
                raise ValueError(msg)

        result_value = note.value - self.hs

        return Note(result_value)

class Chord:
    pass







