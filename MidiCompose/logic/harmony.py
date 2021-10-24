from dataclasses import dataclass
from typing import Optional, Union, Literal

from icecream import ic

from MidiCompose.logic import CONSTANTS as C

# TODO : string representation (mappers.py)
class Note:
    """
    Represents a midi-note.
    - `value` is the midi-compatible attribute (integer between 0-127).
    """

    def __init__(self, note: Union[int,str], verbose: bool = False):
        """
        Parameter `note` can take one of two options:
            1) An integer between 0-127
            2) the string representation of a note. Note that if a string is passed, it
               must either be accompanied by the register of the note (ie. "Eb4" represents
               Eb in the fourth octave).

        :param note:
        :param verbose:
        """

        self._parse_arg(note)

        self.value: int

        self.letter_oct: Optional[str] = None
        self.letter: Optional[str] = None

        self.verbose: bool = verbose

    def _parse_arg(self,note):

        valid_type_set = {int,str}
        if type(note) not in valid_type_set:
            msg = "Parameter `note` must either be an integer between 0-127, or a valid" \
                  "string representation of a note."
            raise TypeError(msg)

        elif type(note) == int:
            if note not in range(128):
                msg = "If `note` is given as an integer, must be between 0-127."
                raise ValueError(msg)
            else:
                self.value = note

        elif type(note) == str:
            pass

    #### SPECIAL METHODS ####
    def __eq__(self, other):
        if type(other) == int:
            if self.value == other:
                return True
            else:
                return False
        else:
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
        else:
            r = f"MidiNote({self.value})"

        return r

class Interval:
    """
    The distance between two notes.

    Can be uniquely identified by:
        - `hs`: number of halfsteps
        - `string`: string representation...eg] "M3+" -> "major third up an octave" -> 16 half-steps

    Either of the unique representations can be supplied as an argument to the constructor.
    """

    def __init__(self, interval: Union[int, str], verbose: bool = True):
        """

        :param interval: Takes one of two options:
                            1) number of half steps (integer)
                            2) string representation...eg] "M3", "P5+", etc.
        :param verbose: If True, __repr__ gives more info.
        """

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
        Given a valid note representation, return a Note object at the appropriate interval.

        :param note: Note object or valid "Note-like" representation.
        :return: Note object at the appropriate interval.
        """
        # coerce to Note object
        if not isinstance(note, Note):
            try:
                note = Note(note)
            except:
                msg = f"`{note}` is an invalid argument."
                raise ValueError(msg)

        result_value = note.value + self.hs

        return Note(result_value)

    def below(self, note:Union[Note, int, str]) -> Note:
        """
        Given a valid note representation, return a Note object at the appropriate interval.

        :param note: Note object or valid "Note-like" representation.
        :return: Note object at the appropriate interval.
        """

        # coerce to Note object
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







