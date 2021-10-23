from typing import Optional, Iterable, Any, Union, Tuple, List
import copy

import numpy as np
from icecream import ic
from numpy.typing import ArrayLike


class TimeUnit:
    """
    Subdivision(state: Union[0,1,2])
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
    Container for TimeUnits. Subdivision attribute determines number of
    TimeUnits.

    Argument `beat` must either be a single integer representing the
    number of subdivisions, or an iterable of TimeUnit or TimeUnit-compatible
    integers (ie. {0,1,2}). The latter is useful when passing stateful TimeUnits.

    Beat(subdivision=4,time_units: array)
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
                msg = "If giving an iterable for `beat`, each element must either be an" \
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

    Two options for initialization:
    1) Supply `n_beats` AND `subdivision`. Will fill the Measure with `inactive` beats.
    2) Supply an iterable of Beat objects
    """

    def __init__(self,
                 n_beats: Optional[int] = None,
                 subdivision: Optional[int] = None,
                 beats: Optional[Iterable[Beat]] = None,
                 verbose: bool = False):

        self._parse_arg(n_beats, subdivision, beats)

        self.beats: ArrayLike[Beat]
        self.n_beats: int

        self.verbose: bool = False

    def _parse_arg(self, n_beats, subdivision, beats):

        if beats is not None:

            arg_set = {n_beats,subdivision}
            if not arg_set.issubset({None}):
                msg = "Arguments given for both `beats` and [`n_beats` and/or `subdivision`]."
                raise AttributeError(msg)
            else:
                if not set([type(b) for b in beats]).issubset({Beat}):
                    msg = "Argument `beats` must only consist of Beat objects."
                    raise TypeError(msg)
                else:
                    self.beats = np.array(beats)
                    self.n_beats = self.beats.size

        elif beats is None:
            if any([n_beats, subdivision]) is None:
                msg = "If `beats` is not given, then both `n_beats` AND `subdivision` are required."
                raise AttributeError(msg)

            else:  # infer n_beats and subdivision
                self.n_beats = n_beats
                self.beats = np.array(Beat(subdivision) * 4)

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
