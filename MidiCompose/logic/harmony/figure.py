from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from itertools import chain
import random
from typing import Optional, Union, List, Tuple, Sequence, Any
from abc import ABC, abstractmethod, abstractproperty
import bisect

from icecream import ic

from MidiCompose.logic.harmony.interval import Interval, sequence_to_intervals
from MidiCompose.logic.harmony.key import KeyFamily, to_key
from MidiCompose.logic.harmony.note import Note, to_note, HasNotes, sequence_to_notes



class BaseFigure:
    """
    Represents number of "steps" steps_above and steps_below a note. When inherited by ChromaticFigure,
    steps represent chromatic half-steps. When inherited by TonalFigure, steps represent
    steps within the given key.
    """
    def __init__(self,
                 steps_above: Optional[Sequence[int]] = None,
                 steps_below: Optional[Sequence[int]] = None):

        self.steps_above = steps_above
        self.steps_below = steps_below

    @property
    def steps_above(self) -> List[int]:
        return self._steps_above

    @steps_above.setter
    def steps_above(self, above):
        _above = None
        if isinstance(above,Sequence):
            if all([isinstance(n,int) and 0 < n < 127 for n in above]):
                _above = above
        elif above is None:
            _above = []

        if _above is None:
            e = "Parameter `steps_above` must be given a sequence of integers."
            raise ValueError(e)
        else:
            self._steps_above = _above

    @property
    def steps_below(self) -> List[int]:
        return self._steps_below

    @steps_below.setter
    def steps_below(self, below):

        _below = None
        if isinstance(below, Sequence):
            if all([isinstance(n, int) and 0 < n < 127 for n in below]):
                _below = below
        elif below is None:
            _below = []

        if _below is None:
            e = "Parameter `steps_below` must be given a sequence of integers."
            raise ValueError(e)
        else:
            self._steps_below = _below

    @property
    def state(self) -> List[int]:
        _state = sorted([-1*n for n in self.steps_below] + [0] +
                        [n for n in self.steps_above])
        return _state

    @property
    def index(self) -> int:
        return self.state.index(0)

    def reindex(self, index: int):

        if index not in range(len(self.state)):
            e = f"Index out of range for figure with {len(self.state)} elements."
            raise ValueError(e)

        idx_element = self.state[index]
        if idx_element == 0:
            _state = self.state
        elif idx_element > 0:
            _state = [n-idx_element for n in self.state]
        else:  # idx_element is negative
            _state = [n-idx_element for n in self.state]

        _above = _state[index+1:]
        _below = [n*-1 for n in _state[:index]]

        _bf = BaseFigure(steps_above=_above, steps_below=_below)

        return _bf

    def __eq__(self,other: BaseFigure):
        if isinstance(other,BaseFigure):
            _self = self.reindex(0)
            _other = other.reindex(0)
            if _self.state == other.state:
                return True
            else:
                return False
        else:
            return False

    def __len__(self):
        _len = len(self.steps_above) + len(self.steps_below)
        return _len + 1

    def __repr__(self):
        above = self.steps_above
        below = self.steps_below
        index = self.index

        r = f"BaseFigure(steps_above={above}, steps_below={below}, index={index})"

        return r

class TonalFigure:

    def __init__(self,
                 note: Union[Note, Any],
                 key: Union[KeyFamily, Any],
                 above: Optional[Sequence[int]] = None,
                 below: Optional[Sequence[int]] = None):
        # setters
        self.above = above
        self.below = below
        self.key = key
        self.note = note

        self.base_figure = BaseFigure(steps_above=[n-1 for n in self.above],
                                      steps_below=[n-1 for n in self.below])

    @property
    def key(self) -> KeyFamily:
        return self._key

    @key.setter
    def key(self, key):
        if isinstance(key, KeyFamily):
            _key = key
        else:
            try:
                _key = to_key(key)
            except:
                raise
        self._key = _key

    @property
    def note(self) -> Note:

        return self._note

    @note.setter
    def note(self,note):
        if isinstance(note,Note):
            _note = note
        else:
            _note = to_note(note)

        if _note not in self.key:
            e = f"Note {_note.as_letter()} not in KeyFamily {self.key.family.as_letter(include_range=False)}."
            raise ValueError(e)

        self._note = _note

    @property
    def above(self) -> List[int]:
        return self._above

    @above.setter
    def above(self,above):
        if above is None:
            above = []
        elif not all([isinstance(n, int) for n in above]):
            e = f"`above` must be a sequence of integers."
            raise ValueError(e)

        self._above = sorted(above)

    @property
    def below(self) -> List[int]:
        return self._below

    @below.setter
    def below(self,below):
        if below is None:
            below = []
        elif not all([isinstance(n,int) for n in below]):
            e = "`below` must be a sequence of integers."
            raise ValueError(e)

        self._below = sorted(below,reverse=True)

    @property
    def index(self):
        return self.base_figure.index

    @property
    def notes_above(self) -> List[Note]:
        _steps_above = self.base_figure.steps_above
        _key = self.key
        _note = self.note
        notes_above = [_key.steps_above(_note, steps=key_steps) for key_steps in _steps_above]
        return notes_above

    @property
    def notes_below(self) -> List[Note]:
        _steps_below = self.base_figure.steps_below
        _key = self.key
        _note = self.note
        notes_below = [_key.steps_below(_note,steps=key_steps)
                       for key_steps in _steps_below]
        return notes_below

    @property
    def notes(self) -> List[Note]:
        _notes = self.notes_below + [self.note] + self.notes_above
        return _notes

    #### UTILITY METHODS ####

    def reindex(self,index: int):
        if index not in range(len(self) + 2):
            e = f"`index` {index} invalid for TonalFigure with size {len(self)}."
            raise ValueError(e)

        _note = self.notes[index]
        _key = self.key

        _bf = self.base_figure

        _bf = _bf.reindex(index)
        _above = [n + 1 for n in _bf.steps_above]
        _below = [n + 1 for n in _bf.steps_below]

        tf = TonalFigure(note=_note,key=_key,above=_above,below=_below)

        return tf

    def to_key(self,
               key: Union[KeyFamily,Any],
               index: Optional[int] = None):
        """
        """
        try:
            key = to_key(key)
        except:
            raise

        if index is None:
            index = self.index

        try:
            tf = self.reindex(index)
        except:
            raise

        _note = tf.note
        _above = tf.above
        _below = tf.below

        if _note not in key:
            e = f"Indexed note `{_note}` not in given key `{key.family.as_letter(include_range=False)}`."
            raise ValueError(e)

        tf = TonalFigure(note=_note,key=key,
                         above=_above,below=_below)

        return tf

    def from_base_figure(self, base_figure: BaseFigure):

        above = [n + 1 for n in base_figure.steps_above]
        below = [n + 1 for n in base_figure.steps_below]

        _note = self.note
        _key = self.key

        return TonalFigure(note=_note,key=_key,above=above,below=below)


    def __len__(self):
        return len(self.above) + len(self.below) + 1

    def __repr__(self):
        note = self.note.as_letter()
        key = self.key.family.as_letter(include_range=False)
        above = self.above
        below = self.below
        notes = [n.as_letter() for n in self.notes]
        index = self.index

        r = f"TonalFigure(note={note}, key={key}, above={above}, below={below}, " \
            f"notes={notes}, index={index})"

        return r


