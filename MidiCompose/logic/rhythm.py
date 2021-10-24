from typing import Optional, Iterable, Any, Union, Tuple, List
import copy

import numpy as np
from icecream import ic
from numpy.typing import ArrayLike


class TimeUnit:
    """
    Contains the state of a subdivision within a Beat.

    State can be 1 (attack), 2 (sustain), or 0 (release).
    """

    def __init__(self,
                 state: Optional[int] = 0,
                 verbose: bool = False):

        # definitive attribute
        self.state: Optional[int] = state
        self._validate()

        # __repr__ verbosity
        self.verbose: bool = verbose

    def _validate(self):
        if not isinstance(self.state, int):
            msg = "`state` must be an integer."
            raise TypeError(msg)
        if self.state not in {0, 1, 2}:
            msg = "`state` can only be either 0, 1, or 2."
            raise ValueError(msg)

    def activate(self):
        self.state = 1

    def sustain(self):
        self.state = 2

    def deactivate(self):
        self.state = 0

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def __repr__(self):
        if self.verbose:
            r = f"TimeUnit(state={self.state})"
        else:
            r = str(self.state)
        return r

class BeatIterator:

    def __init__(self, beat):
        self._Beat = beat
        self._index = 0

        self._len_Beat = self._Beat.subdivision

    def __next__(self):
        if self._index < self._len_Beat:
            result = self._Beat.time_units[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

# TODO: include TimeUnit ordering rules in Beat._validate()
class Beat:
    """
    Container for TimeUnit objects.

    Definitive attribute is `self.beats`, which is a numpy array containing TimeUnit objects.

    Argument `beat` must either be a single integer representing the number of
    subdivisions, or an iterable containing TimeUnit objects and/or "TimeUnit-like"
    integers (ie. {0,1,2}). The latter is useful when passing stateful TimeUnit objects.
    """

    def __init__(self,
                 beat: Union[int, Iterable[Union[int, TimeUnit]]] = 1,
                 verbose: bool = False):

        self._parse_beat_arg(beat)

        self.time_units: ArrayLike[TimeUnit]
        self.subdivision: int

        self.verbose = verbose

        self._validate()

    def _parse_beat_arg(self, beat):
        """
        Argument `beat` must either be a single integer representing the
        number of subdivisions, or an iterable of TimeUnit or TimeUnit-compatible
        integers (ie. {0,1,2}).
        """

        # if integer, `beat` represents number of subdivisions
        if isinstance(beat, int):
            self.subdivision = beat
            self._init_time_units()

        # else, `beat` represents iterable of TimeUnit-like objects
        else:
            beat_set = set([type(a) for a in beat])
            valid = {int, TimeUnit}
            if not beat_set.issubset(valid):
                msg = "If giving an iterable for `beat`, each element must either be an " \
                      "integer in {0,1,2} or a TimeUnit object"
                raise TypeError(msg)
            if beat_set == {TimeUnit}:
                time_units = beat
            else:
                time_units = []
                for item in beat:
                    if isinstance(item, TimeUnit):
                        time_units.append(item)
                    else:
                        tu = TimeUnit(item)
                        time_units.append(tu)
            self.time_units = np.array(time_units)
            self.subdivision = self.time_units.size

    def _validate(self):

        # subdivision must be >= 1
        if self.subdivision < 1:
            msg = "`subdivision` must be >= 1."
            raise ValueError(msg)

    def _init_time_units(self):
        """
        Initializes deactivated TimeUnit objects based on subdivision.
        """
        self.time_units = np.array([TimeUnit() for _ in range(self.subdivision)])

    def set_verbosity(self, verbose: bool):
        self.verbose = verbose

    def is_active(self) -> bool:
        """
        Returns True if any TimeUnit instances contain active state (1 or 2).
        Otherwise, returns False.
        """
        if self.time_units.all() == 0:
            return False
        else:
            return True

    def __repr__(self):
        r = f"Beat(subdivision={self.subdivision}"
        if self.verbose:
            tus = []
            for tu in self.time_units:
                tu.set_verbose(False)
                tus.append(tu)
            r += f",\n     time_units={str(tus)}"
        r += ")"
        return r

    def __iter__(self):
        return BeatIterator(self)

    def __getitem__(self, item) -> TimeUnit:
        return self.time_units[item]

    def __mul__(self, number: int):
        copies = []
        for _ in range(number):
            copies.append(copy.deepcopy(self))
        return copies

class MeasureIterator:

    def __init__(self, measure):
        self._Measure = measure
        self._index = 0
        self._len_Measure = self._Measure.n_beats

    def __next__(self):
        if self._index < self._len_Measure:
            result = self._Measure.beats[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

class Measure:
    """
    Container for Beats.

    Three options for initialization:
    1) Supply iterable of Beat object. This is useful if passing Beats with pre-defined state.
    2) Supply an iterable integers, where the number of items represents the number of beats,
    and the values of the integers represents the respective subdivision of each beat.
    3) Combination of the previous two.

    Note that passing an integer will automatically instantiate an "empty" beat. That is,
    all TimeUnit objects will be set to 0 within that beat.
    """

    def __init__(self,
                 beats: Union[Iterable[Beat],Iterable[int]],
                 verbose: bool = False):
        """
        Three options for initialization:
        1) Supply iterable of Beat object. This is useful if passing Beats with pre-defined state.
        2) Supply an iterable integers, where the number of items represents the number of beats,
        and the values of the integers represents the respective subdivision of each beat.
        3) Combination of the previous two.

        Note that passing an integer will automatically instantiate an "empty" beat. That is,
        all TimeUnit objects will be set to 0 within that beat.

        :param beats: iterable containing Beat objects, bare integers, or a combination of the two.
        :param verbose: if True, __repr__ gives more info.
        """

        self._parse_arg(beats)

        self.beats: ArrayLike[Beat]
        self.n_beats: int

        self.verbose: bool = False

    def _parse_arg(self, beats):

        arg_set = set([type(a) for a in beats])

        beat_set = {Beat}
        int_set = {int}
        mixed_set = {Beat,int}

        # validate type-set of `beats` arg
        if arg_set.isdisjoint(mixed_set):
            msg = "Argument `beats` must be an iterable containing only integers and/or " \
                  "Beat objects."
            raise AttributeError(msg)

        # contains only Beats -- no validation needed
        elif arg_set.issubset(beat_set):
            self.beats = np.array(beats)
            self.n_beats = self.beats.size

        # contains only integers -- validated by Beat constructor
        elif arg_set.issubset(int_set):
            self.beats = np.array([Beat(a) for a in beats])
            self.n_beats = self.beats.size

        # contains mixture Beat and int -- validated by Beat constructor
        else:
            _beats = []
            for b in beats:
                if type(b) == int:
                    _beats.append(Beat(b))
                else:
                    _beats.append(b)
            self.beats = np.array(_beats)
            self.n_beats = self.n_beats.size


        # validate arg types
        if not arg_set.issubset(mixed_set):
            msg = "Argument `beats` must be an iterable containing Beat objects and/or itegers."
            raise AttributeError(msg)

    #### ACTIVATION FUNCTIONS ####
    def __iter__(self):
        return MeasureIterator(self)

    def __getitem__(self, item: int) -> Beat:
        return self.beats[item]

    def __repr__(self):
        if self.verbose:
            r = "IMPLEMENT VERBOSE"
            return r
        else:
            m = list()
            for beat in list(self.beats):
                b = list()
                for tu in beat:
                    # tu.set_verbose(False)
                    b.append(tu)
                m.append(str(b))
            r = "\n".join(m)

            return r


class Part:
    """
    Container for Measures
    """


class Score:
    """
    Container for parts
    """
