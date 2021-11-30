from typing import Union, Optional
from icecream import ic

from MidiCompose.logic.harmony import note_mapping as nm


class Note:
    """
    Represents a midi-note
    """

    def __init__(self, note: Union[int, str], accidental: Optional[str] = None):
        """
        :param note: - Either an integer between (0-127)
                     - or a letter-representation between ("C-2" and "G8")
        """
        self.value: int = note  # calls setter
        self.accidental = accidental  # calls setter

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v: Union[int, str]):

        if type(v) == int:
            if v not in range(128):
                msg = "`note` must be within range (0-127) if being passed as an integer."
                raise ValueError(msg)
            else:
                self._value = v

        elif type(v) == str:
            self._value = nm.letter_to_value(v)

        else:
            msg = "Invalid argument. `note` must be a valid integer or string representation of a note."
            raise ValueError(msg)

    @property
    def accidental(self):
        return self._accidental

    @accidental.setter
    def accidental(self, v: Optional[str] = None):
        if v not in {None, "sharp", "flat"}:
            msg = f"Invalid argument for `Note.accidental`. `accidental` must be one of {{None,'sharp','flat'}}. Given {v} "
            raise ValueError(msg)
        else:
            self._accidental = v

    #### UTILITY METHODS ####
    def as_letter(self, accidental: Optional[str] = None) -> str:
        """
        Returns letter representation of Note.
        """
        letter = nm.value_to_letter(value=self.value,
                                    accidental=accidental)
        return letter

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

    def __hash__(self):
        return hash(self.value)

    def __lt__(self, other):
        if type(other) == int:
            if self.value < other:
                return True
            else:
                return False

        elif type(other) == Note:
            if self.value < other.value:
                return True
            else:
                return False

    def __gt__(self, other):
        if type(other) == int:
            if self.value > other:
                return True
            else:
                return False

        else:
            if self.value > other.value:
                return True
            else:
                return False

    def __le__(self, other):
        if type(other) == int:
            if self.value <= other:
                return True
            else:
                return False
        else:
            if self.value <= other.value:
                return True
            else:
                return False

    def __ge__(self, other):
        if type(other) == int:
            if self.value >= other:
                return True
            else:
                return False
        else:
            if self.value >= other.value:
                return True
            else:
                return False

    def __ne__(self, other):
        if self.value != other.value:
            return True
        else:
            return False

    def __add__(self, other):
        if type(other) == int:
            value = self.value + other
        else:
            value = self.value + other.value
        try:
            return Note(value)
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
        r = f"Note({self.as_letter()})"
        return r
