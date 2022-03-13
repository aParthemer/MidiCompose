from __future__ import annotations

from copy import deepcopy
from itertools import cycle
from typing import Set, List, Union, Sequence, Tuple, Any, Optional
from enum import Enum
from icecream import ic

from MidiCompose.logic.harmony.interval import Interval
from MidiCompose.logic.harmony.note import Note, HasNotes, to_note, sequence_to_notes


class KeyFamily:
    schema = [2, 2, 1, 2, 2, 2]

    def __init__(self, family: Union[Note, int, str]):

        self.family = family  # calls setter

    @property
    def family(self) -> Note:
        return self._family

    @family.setter
    def family(self, value):

        if not isinstance(value, Note):
            try:
                _family = Note(value)
            except:
                raise
        else:
            _family = value

        self._family = _family

    @property
    def notes(self) -> List[Note]:

        # get major scale based on family
        _family = Note(self.family.value % 12)

        _scale = [_family]
        for interv in self.schema:
            next_note = Note((_scale[-1].value + interv) % 12)
            _scale.append(next_note)

        return _scale

    def get_neighbors(self, depth=1) -> List[Tuple[Any, Any]]:

        if 1 > depth > 6:
            e = "`depth` must be between 1 and 6"
            raise ValueError(e)

        _family = self.family

        _neighbors = []
        for _ in range(depth):
            if len(_neighbors) == 0:
                upper_neighbor = Interval("P5").above(_family)
                lower_neighbor = Interval("P4").above(_family)

                _upper_kf = deepcopy(self)
                _lower_kf = deepcopy(self)

                _upper_kf.family = upper_neighbor
                _lower_kf.family = lower_neighbor

                _neighbors.append((_lower_kf, _upper_kf))
            else:
                lower_note = _neighbors[-1][0].family
                upper_note = _neighbors[-1][1].family

                lower_neighbor = Interval("P4").above(lower_note)
                upper_neighbor = Interval("P5").above(upper_note)

                _lower_kf = deepcopy(_neighbors[-1][0])
                _upper_kf = deepcopy(_neighbors[-1][1])

                _lower_kf.family = lower_neighbor
                _upper_kf.family = upper_neighbor

                _neighbors.append((_lower_kf, _upper_kf))

        return _neighbors

    def get_index_of(self,
                     note: Union[Note, int, str]) -> int:

        try:
            _note = to_note(note)
        except:
            raise

        if _note not in self:
            e = f"Given note `{note}` is not in KeyFamily `{self.family}`"
            raise ValueError(e)

        _note = Note(_note.value % 12)

        return self.notes.index(_note)

    def next_note(self,
                  note: Union[Note, int, str],
                  step: int = 1) -> Note:

        if step <= 0:
            e = "Argument `step` must be >= 1."
            raise ValueError(e)
        else:
            try:
                _note = to_note(note)
            except:
                raise

            try:
                _idx = self.get_index_of(note)
            except:
                raise

        for _step in range(step):
            _idx = (_idx + 1) % len(self.notes)
            _next_note = self[_idx]

        return _next_note

    def previous_note(self,
                      note: Union[Note, int, str],
                      step: int = 1) -> Note:
        if step <= 0:
            e = "Argument `step` must be >= 1."
            raise ValueError(e)
        else:
            try:
                _note = to_note(note)
            except:
                raise
            try:
                _idx = self.get_index_of(note)
            except:
                raise

            for _step in range(step):
                _idx = (_idx - 1) % len(self.notes)
                _previous_note = self[_idx]

        return _previous_note

    def note_range(self,
                   a: Union[Note,Any],
                   b: Union[Note,Any]) -> List[Note]:
        """
        order is preserved
        """
        try:
            a,b = [to_note(n) for n in [a,b]]
        except:
            raise

        if a == b:
            return [a]
        else:
            chrom_range = Note.range(a,b)
            rng = [n for n in chrom_range if n in self]
            return rng

    def steps_above(self,
                    note: Union[Note, int, str],
                    steps: int) -> Note:
        """
        Get the Note which is "N" steps away from the given note in the context of the current Key.
        """

        try:
            _note = to_note(note)
        except:
            raise
        try:
            _idx = self.get_index_of(note)
        except:
            raise

        if steps < 0:
            e = "Argument `steps` must be positive."
            raise ValueError(e)

        _previous = _note
        for _ in range(steps):
            _n = self.next_note(_previous)
            _previous = _previous.nearest_neighbors(_n, "UPPER")

        _final = _previous
        return _final

    def steps_below(self,
                    note: Union[Note, int, str],
                    steps: int) -> Note:
        try:
            _note = to_note(note)
        except:
            raise
        try:
            _idx = self.get_index_of(note)
        except:
            raise

        if steps < 0:
            e = "Argument `steps` must be positive."
            raise ValueError(e)

        _previous = _note
        for _ in range(steps):
            _n = self.previous_note(_previous)
            _previous = _previous.nearest_neighbors(_n, "LOWER")

        _final = _previous
        return _final

    def steps_between(self,
                      a:Note,
                      b:Note) -> int:
        """
        Returns the number of scale-steps between two notes in a key. Direction is assumed as from `a` to `b`.
        """
        try:
            a,b = to_note(a),to_note(b)
            _notes = [a,b]

        except:
            raise

        if any([n not in self for n in _notes]):
            bad = [n for n in _notes if n not in self]
            e = f"The given note(s) `{bad}` do not exist in the KeyFamily `{self.family}`."
            raise ValueError(e)

        else:
            steps = 0
            _dir = 1
            if a == b:
                pass
            elif a < b:
                while a < b:
                    a = self.steps_above(a,1)
                    steps += 1
            elif a > b:
                _dir = -1
                while a > b:
                    a = self.steps_below(a,1)
                    steps += 1

            steps = steps * _dir

            return steps

    @staticmethod
    def all_keys_with(notes: Union[Note, int, str, Sequence],
                      _any: bool = False,
                      _raise: bool = False):
        """
        Returns a list of KeyFamily instances which contain `notes`.
        :param notes: One or many Note/note-like objects
        :param _any: if True, will return all keys containing any of the given notes. Default behavior is to include only
        keys which contain all `notes`
        """
        _all_notes = list(range(0, 12))
        _all_keys = [KeyFamily(n) for n in _all_notes]

        if isinstance(notes,Sequence):
            try:
                _notes = sequence_to_notes(notes)
            except:
                raise
        else:
            try:
                _notes = [to_note(notes)]
            except:
                raise
        if _any:
            _keys_with = []
            for key in _all_keys:
                if any([n in key for n in _notes]):
                    _keys_with.append(key)
        else:
            _keys_with = [k for k in _all_keys if _notes in k]

        if len(_keys_with) == 0 and _raise:
            e = f"Given notes {_notes} do not exist in any Key."
            raise ValueError(e)

        return _keys_with

    @staticmethod
    def all_keys() -> List[KeyFamily]:
        """
        Returns a list of all Keys
        """
        return [KeyFamily(n) for n in range(12)]

    def __getitem__(self, item):

        if item not in range(0, len(self.notes)):
            e = f"Index must be between 1 and {len(self.notes) - 1}."
            raise IndexError(e)

        return self.notes[item]

    def __contains__(self, item: Union[Note, str, int, Sequence]) -> bool:

        if isinstance(item, Note):

            _item = Note(item.value % 12)

            if _item in self.notes:
                return True
            else:
                return False

        elif isinstance(item, str) or isinstance(item, int):
            try:
                _item = Note(item)
            except:
                raise

            _item = Note(_item.value % 12)
            if _item in self.notes:
                return True
            else:
                return False

        elif isinstance(item, Sequence):
            try:
                _notes = sequence_to_notes(item)
            except:
                raise

            if all([n.signature in self.notes for n in _notes]):
                return True
            else:
                return False

    def __len__(self):
        return len(self.notes)

    def __eq__(self,other):
        if isinstance(other,KeyFamily):
            if other.family == self.family:
                return True
            else:
                return False
        else:
            return NotImplementedError

    def __repr__(self):
        r = f"KeyFamily({self.family.as_letter(include_range=False)}," \
            f" {[n.as_letter(include_range=False) for n in self.notes]}"
        return r


class ModeEnum(Enum):
    IONIAN = MAJOR = 1
    DORIAN = 2
    PHRYGIAN = 3
    LYDIAN = 4
    MIXOLYDIAN = 5
    AEOLIAN = MINOR = 6
    LOCRIAN = 7

class Mode:
    def __init__(self,
                 tonic: Union[Note, Any],
                 mode: Union[ModeEnum, Any]):

        self.tonic = tonic  # setter
        self.mode = mode  # setter

    @property
    def mode(self) -> ModeEnum:
        return self._mode

    @mode.setter
    def mode(self,mode):
        if not isinstance(mode,ModeEnum):
            if isinstance(mode,str):
                try:
                    _mode = ModeEnum[mode]
                except:
                    raise
            elif isinstance(mode,int):
                try:
                    _mode = ModeEnum(mode)
                except:
                    raise
        else:
            _mode = mode

        self._mode = _mode

    @property
    def tonic(self) -> Note:
        return self._tonic

    @tonic.setter
    def tonic(self,tonic):
        try:
            _tonic = to_note(tonic)
        except:
            raise
        _tonic = Note(_tonic.signature)
        self._tonic = _tonic

    @property
    def key_family(self) -> KeyFamily:
        _mode_val = self.mode.value
        _tonic = self.tonic

        possible_keys = KeyFamily.all_keys_with(notes=[_tonic])
        _key = [key for key in possible_keys if key.get_index_of(_tonic) == _mode_val-1][0]
        return _key

    @property
    def notes(self) -> List[Note]:
        _notes = self.key_family.notes
        print(_notes)
        _tonic = self._tonic
        print(_tonic)

        start_idx = _notes.index(_tonic)
        front = _notes[start_idx:]
        back = _notes[:start_idx]

        _notes = front + back
        return _notes

    def __repr__(self):
        r = f"Mode({self.mode.name}, tonic={self.tonic.as_letter(include_range=False)}," \
            f" key_family={self.key_family.family.as_letter(include_range=False)})"
        return r




#### VALIDATORS ####

def to_key(key_like):
    if isinstance(key_like, KeyFamily):
        return key_like
    elif isinstance(key_like, Note):
        return KeyFamily(key_like)
    elif isinstance(key_like, str):
        try:
            kf = KeyFamily(key_like)
            return kf
        except:
            raise


