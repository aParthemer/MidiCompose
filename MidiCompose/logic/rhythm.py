from typing import Optional, Iterable, Any, Union, Tuple, List, Collection
import copy

import numpy as np
from icecream import ic
from numpy.typing import ArrayLike


class TimeUnit:
    """
    Contains the time_units of a subdivision within a Beat.

    State can be 1 (attack), 2 (sustain), or 0 (release).
    """

    def __init__(self,
                 state: int = 0,
                 verbose: bool = False):

        # definitive attribute
        self.state: int = state
        self._validate()

        # __repr__ verbosity
        self.verbose: bool = verbose

    def _validate(self):
        if not isinstance(self.state, int):
            msg = "`time_units` must be an integer."
            raise TypeError(msg)
        if self.state not in {0, 1, 2}:
            msg = "`time_units` can only be either 0, 1, or 2."
            raise ValueError(msg)

    def activate(self):
        self.state = 1

    def sustain(self):
        self.state = 2

    def deactivate(self):
        self.state = 0

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def __eq__(self, other):
        if type(other) == int:
            return self.state == other
        else:
            return self.state == other.time_units

    def __int__(self):
        return int(self.state)

    def __repr__(self):
        if self.verbose:
            r = f"TimeUnit(time_units={self.state})"
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

    Definitive attribute is `self.time_units`, which is a numpy array containing TimeUnit objects.

    Argument `beat` must either be a single integer representing the number of
    subdivisions, or an iterable containing TimeUnit objects and/or "TimeUnit-like"
    integers (ie. {0,1,2}). The latter is useful when passing stateful TimeUnit objects.
    """

    def __init__(self,
                 beat: Union[int, Iterable[Union[int, TimeUnit]]] = 1,
                 verbose: bool = False):
        """
        :param verbose: determines format of output
        """

        self._parse_beat_arg(beat)

        self.time_units: ArrayLike[TimeUnit]

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
            self.time_units = np.array([TimeUnit() for _ in range(beat)])
            self.state = self.time_units

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
            self.state = self.time_units

    def _validate(self):

        # subdivision must be >= 1
        if self.subdivision < 1:
            msg = "`subdivision` must be >= 1."
            raise ValueError(msg)

    @property
    def subdivision(self) -> int:
        return self.time_units.size

    @property
    def state(self) -> np.ndarray:
        """
        1d numeric array representing the state of each TimeUnit in the Beat.
        """
        return self._state

    @state.setter
    def state(self,value):
        self._state = np.array([int(n) for n in value])

    @property
    def is_active(self) -> bool:
        """
        Returns True if any TimeUnit instances contain active time_units (1 or 2).
        Otherwise, returns False.
        """
        if self.state.all() == 0:
            return False
        else:
            return True

    #### UTILITY FUNCTIONS ####

    def set_state(self,
                  state: Collection[int],
                  override: bool = False):
        """
        Set the time_units of the TimeUnit instances to either 0,1 or 2.

        :param state: Collection of integers
        :param override: If False, error will be raised if setting time_units to an already active
        """

        # validation
        if not override:
            if self.is_active:
                msg = "Cannot set time_units to an already active beat. If you wish to override" \
                      "the current time_units, set argument `override` to True."
                raise AttributeError(msg)

        valid_set = {0, 1, 2}
        valid_len = self.subdivision
        if len(state) != valid_len:
            msg = "The collection passed to argument `time_units` must have the same number" \
                  "of elements as the number of subdivisions in the Beat."
            raise ValueError(msg)
        elif not set(state).issubset(valid_set):
            msg = "`time_units` can only take a collection containing {0,1,2}"
            raise ValueError(msg)

        self.state = state

    def __iter__(self):
        return BeatIterator(self)

    def __getitem__(self, item) -> TimeUnit:
        return self.state[item]

    def __mul__(self, number: int):
        copies = []
        for _ in range(number):
            copies.append(copy.deepcopy(self))
        return copies

    def set_verbosity(self, verbose: bool):
        self.verbose = verbose

    def __repr__(self):

        if self.verbose:
            r = f"Beat(subdivision={self.subdivision}"
            tus = []
            for tu in self.state:
                tu.set_verbose(False)
                tus.append(tu)
            r += f",\n     time_units={str(tus)}"
            r += ")"
        else:
            r = str(self.state)
        return r


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

    def __init__(self,
                 beats: Union[Collection[Union[int,Beat,Collection[int]]]],
                 verbose: bool = False):
        """
        Three options for initialization:
        1) Supply iterable of Beat object. This is useful if passing Beats with pre-defined time_units.
        2) Supply a collection of collections of integers, where the number of items represents the number
           of time_units, and the values of the integers represents the respective subdivision of each beat.
        3) Combination of the previous two.

        Note that passing an integer will automatically instantiate an "empty" beat. That is,
        all TimeUnit objects will be set to 0 within that beat.

        :param beats: iterable containing Beat objects, bare integers, or a combination of the two.
        :param verbose: if True, __repr__ gives more info.
        """

        self.beats: ArrayLike[Beat] = beats  # calls setter method

        self.verbose: bool = verbose

    @property
    def beats(self):
        return self._beats

    @beats.setter
    def beats(self,value):

        ic(value)
        value_type_set = set([type(b) for b in value])

        beat_set = {Beat}
        int_set = {int}
        col_of_ints_set = {Collection}
        mixed_set = {Beat, int}

        # collection of collections of integers
        coll_of_colls = all([issubclass(type(b), Collection) for b in value])
        if coll_of_colls:
            self._beats = np.array([Beat(c) for c in value])

        # contains only Beats -- no validation needed
        elif value_type_set.issubset(beat_set):
            self._beats = np.array(value)

        # contains only integers -- validated by Beat constructor
        elif value_type_set.issubset(int_set):
            self._beats = np.array([Beat(a) for a in value])

        # contains mixture Beat and int -- validated by Beat constructor
        else:
            _beats = []
            for b in value:
                if type(b) == int:
                    _beats.append(Beat(b))
                else:
                    _beats.append(b)
            self._beats = np.array(_beats)

    @property
    def state(self):
        """
        1-d numeric array containing state of each beat in Measure.
        """
        beat_list = self.beats.tolist()
        state = np.array([b.state for b in beat_list])
        return state

    @property
    def n_beats(self):
        return self.beats.shape[0]

    @property
    def is_active(self):
        pass

    #### UTILITY FUNCTIONS ####
    # TODO: implement override/reshape checks
    def set_state(self,
                  state: [Collection[Collection[int]]],
                  override: bool = True,
                  reshape: bool = False):
        """
        Sets `state` array as well as `beats` array.

        :param override: If False, will raise exception if trying to override a stateful measure.
        :param reshape: If False, will raise exception if `state` argument would result in "reshaping"
                        the measure (ie. changing the number of beats, or number of subdivisions in a beat.)
        """
        self.beats = state

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
            for beat in list(self.state):
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
    pass


class Score:
    """
    Container for parts
    """
