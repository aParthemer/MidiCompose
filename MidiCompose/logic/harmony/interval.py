from typing import Union, Optional

from icecream import ic

from MidiCompose.logic.harmony import interval_mapping as imap
from MidiCompose.logic.harmony.note import Note


class Interval:
    """
    The distance between two note_vals.

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
            self.string = imap.INTERVAL_MAPPER[self.hs]

        elif isinstance(interval, str):
            try:
                self.string = interval
                self.hs = imap.INTERVAL_MAPPER[interval]
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

    #### MAGIC METHODS ####

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
        if not type(note) == Note:
            try:
                note = Note(note)
            except:
                msg = f"`{note}` is an invalid argument."
                raise ValueError(msg)

        result_value = int(note.value + self.hs)
        result_note = Note(result_value)

        return result_note

    def below(self, note: Union[Note, int, str]) -> Note:
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

        result_value = int(note.value - self.hs)

        return Note(result_value)