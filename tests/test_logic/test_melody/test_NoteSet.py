from typing import List

import pytest
from icecream import ic

from compositional.logic.harmony.interval import Interval
from compositional.logic.melody import scale
from compositional.logic.melody.note_set import NoteSet
from compositional.logic.harmony.note import Note


@pytest.mark.parametrize(
    ["notes", "expected_len", "int_set", "note_set"],
    [
        ([Note(60), Note(64), Note(67)], 3, {60, 64, 67}, {Note(60), Note(64), Note(67)}),
        ([Note(60), 64, 67, Note("A#3")], 4, {60, 64, 67, 70}, {Note(60), Note(64), Note(67), Note(70)})
    ]
)
def test_constructor(notes, expected_len, int_set, note_set):
    ns = NoteSet(notes=notes)

    assert len(ns) == expected_len
    assert set(ns) == int_set == note_set

    assert type(ns.notes) == list
    assert set([type(n) for n in ns]).issubset({Note})


@pytest.mark.parametrize(
    ["tonic", "scale", "range_above", "range_below", "expected_notes"],
    [
        (Note("C3"), scale.DiatonicModes.MAJOR, Interval(12), Interval(0),
         [Note(n) for n in ["C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4"]]),
        (Note(60), scale.DiatonicModes.MAJOR, Interval("P1+"), Interval("P4"),
         [Note(n) for n in ["G2", "A2", "B2", "C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4"]])
    ])
def test_from_scale(tonic, scale, range_above, range_below,
                    expected_notes):
    ns_scale = NoteSet()
    ns_scale.from_scale(tonic=tonic, scale=scale,
                        range_above=range_above,
                        range_below=range_below)

    assert ns_scale is not None
    assert [n for n in ns_scale] == expected_notes


def test_random_sample():
    ns = NoteSet([60, 64, 67])

    # no args, returns shuffled set
    sample_1 = ns.random_sample()
    assert len(sample_1) == 3
    assert set(sample_1).issubset({Note(60), Note(64), Note(67)})

    # sample size smaller than set, start item specified
    sample_2 = ns.random_sample(n=2, start=Note(60))
    assert len(sample_2) == 2
    assert sample_2[0] == Note(60)
    assert set(sample_2[1:]).issubset({64, 67})

    # sample size larger than set, each cycle gets same starting item
    sample_3 = ns.random_sample(n=60, start=Note(64), _cycle=True, _cycle_start=True)
    _idx_cycle_starts = [0 + 3 * i for i in range(60 // 3)]
    _cycle_start_set = set([sample_3[i] for i in _idx_cycle_starts])

    assert len(sample_3) == 60
    assert sample_3[0] == sample_3[3] == sample_3[6] == 64
    assert _cycle_start_set.issubset({64})

    # sample size larger than set, start item only first element of sample
    sample_4 = ns.random_sample(n=60, start=Note(67), _cycle=True)
    _idx_cycle_starts = [0 + 3 * i for i in range(60 // 3)]
    _cycle_start_set = set([sample_4[i] for i in _idx_cycle_starts])

    assert len(sample_4) == 60
    assert not _cycle_start_set.issubset({Note(67)})
