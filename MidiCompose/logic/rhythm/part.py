from typing import Collection, Optional, List

import numpy as np

from MidiCompose.logic.rhythm.measure import Measure

class PartIterator:

    def __init__(self, part):
        self._Part = part
        self._index = 0
        self._len_Part = self._Part.n_measures

    def __next__(self) -> Measure:
        if self._index < self._len_Part:
            result = self._Part.measures[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

class Part:
    """
    Container for Measures
    """

    def __init__(self, measures: Optional[Collection[Measure]] = None):
        self.measures = measures

    @property
    def measures(self) -> List[Measure]:
        return self._measures

    @measures.setter
    def measures(self, value):

        if value is None:  # initialize empty part
            value = [Measure()]
        self._measures = [measure for measure in value]

    @property
    def state(self):
        measure_states = np.concatenate([m.state for m in self.measures])
        state = np.empty(shape=(measure_states.size + 2,), dtype=np.int8)
        state[0], state[-1] = -1, -1
        state[1:-1] = measure_states
        return state

    @property
    def n_note_on(self) -> int:
        return sum([m.n_note_on for m in self.measures])

    @property
    def n_measures(self) -> int:
        return len(self.measures)

    @property
    def n_beats(self) -> int:
        return sum([m.n_beats for m in self.measures])

    @property
    def active_state(self):
        pass

    #### MAGIC METHODS ####
    def __iter__(self):
        return PartIterator(self)

    def __getitem__(self, item: int) -> Measure:
        return self.measures[item]

    def __len__(self):
        return len(self.measures)

    def __repr__(self):
        header = "Part(["
        r = header
        measure_strings = [str(m) for m in self.measures]
        for m in measure_strings:
            r += "\n" + " "*len(header) + m
        r += "\n    ])"

        return r



