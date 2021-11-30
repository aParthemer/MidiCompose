from typing import List, Union, Optional, Sequence

import numpy as np
from numpy.typing import ArrayLike

from MidiCompose.logic.harmony.note import Note
import collections

class MelodyIterator:

    def __init__(self, melody):
        self._Melody = melody
        self._index = 0
        self._len_Melody = len(self._Melody)

    def __next__(self) -> Note:
        if self._index < self._len_Melody:
            result = self._Melody[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration


class Melody:
    """
    A collection of Note objects with utility functions for generating melodies.
    """

    def __init__(self,
                 notes: Optional[Union[Sequence[Note], Sequence[int]]] = None,
                 velocity: Union[int,Sequence[int]] = 64):
        """

        :param notes:
        :param velocity: If given single integer, all Notes will be given same velocity. Otherwise, `velocity` must be
        an array of integers with size equal to the number of notes.
        """

        self.notes = notes  # calls setter

        self.velocity = velocity # calls setter

    @property
    def notes(self) -> List[Note]:
        return self._notes

    @notes.setter
    def notes(self, value):

        final_typeset = {Note}

        if value is None:
            self._notes = list()

        elif isinstance(value, list):

            type_set = set([type(n) for n in value])

            if type_set.issubset(final_typeset):  # already list of notes
                self._notes = value
            elif type_set.issubset({Note, int}):  # collection of Note and int
                _notes = []
                for n in value:
                    if isinstance(n, Note):
                        _notes.append(n)
                    elif isinstance(n, int):
                        _notes.append(Note(n))
                self._notes = _notes
        else:
            msg = f"Unrecognized argument: {value}"
            raise ValueError(msg)

    @property
    def velocity(self) -> np.ndarray:
        return self._velocity

    @velocity.setter
    def velocity(self,value):

        _velocity = None
        # if single integer
        if isinstance(value,int):
            _velocity = np.full(shape=len(self),fill_value=value)

        # if numpy array
        elif isinstance(value,np.ndarray):
            if not value.shape == (len(self),):  # invalid size
                msg = f"`self.velocity` must either be a single integer, or a Sequence of integers with" \
                      f"size equal to the number of notes in `self.notes`."
                raise ValueError(msg)
            elif not ((value >= 0) & (value <= 127)).all():  # invalid range
                msg = f"`velocity` must be in range (0,127)"
                raise ValueError(msg)
            else:
                _velocity = value

        # if sequence of integers
        elif isinstance(value,collections.Sequence):
            if not len(value) == len(self):  # invalid size
                msg = f"`self.velocity` must either be a single integer, or a Sequence of integers with" \
                      f"size equal to the number of notes in `self.notes`."
                raise ValueError(msg)
            elif set([type(v) for v in value]) != {int}:  # not all integers
                msg = "`self.velocity` can only take integer values."
                raise ValueError(msg)
            elif not all([v in range(128) for v in value]):
                msg = f"All values in `self.velocity` must be in range (0,127)"
                raise ValueError(msg)
            else:
                _velocity = np.array(value)

        self._velocity = _velocity

    #### MAGIC METHODS ####
    def __len__(self):
        return len(self.notes)

    def __getitem__(self, item: int):
        return self.notes[item]

    def __iter__(self):
        return MelodyIterator(self)

    def __repr__(self):
        r = "Melody("
        r += ", ".join([str(n.value) for n in self.notes])
        r += ")"
        return r



