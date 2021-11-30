import numpy as np
from icecream import ic as ice

from MidiCompose.logic.harmony.note import Note
from MidiCompose.logic.rhythm.part import Part
from MidiCompose.translation.track_builder import TrackBuilder

from MidiCompose.logic.melody import NOTE_SETS as NS

from tests.test_objects import rhythm_obj as ro
from tests.test_objects import melody_obj as mo

import pytest




@pytest.mark.parametrize(
    ["parts", "melodies"],
    [
        # single part, single note
        ([ro.p_m1_m2], [Note(60)]),
        # single part, multi-note
        ([ro.p_m1_m2], [Note(60), Note(64), Note(65)]),
        # multi-part, multi-note
        ([ro.p_m1_m2, ro.p_m1_m3], [Note(60), Note(64)]),
    ]
)
def test_melodies_from_Note_sequence(parts, melodies):
    # instantiate TrackBuilder
    sp = TrackBuilder(parts=parts,
                      melodies=melodies)

    if sp.is_multi_part:
        assert len(sp.parts) == len(sp.melodies)

        for melody, part in zip(sp.melodies, sp.parts):
            # each melody consists of only one item
            assert len(set(melody)) == 1
            # each melody same size as corresponding part
            assert len(melody) == part.n_note_on

    else:  # when single part, multi melodies
        for melody in sp.melodies:
            assert len(set(melody)) == 1
            assert len(melody) == sp.parts[0].n_note_on


@pytest.mark.parametrize(
    ["parts", "melodies", "n_parts", "n_melodies"],
    [  # single part, single melody
        ([ro.p_b__4_note_on__4],
         [mo.mel_cycle_scale(n_notes=4, tonic=Note("C3"), scale=NS.DiatonicModes.MAJOR)],
         1, 1),
        # single part, multiple melodies
        ([ro.p_b__4_note_on__4],
         [mo.mel_cycle_scale(4, tonic=Note("C3"), scale=NS.DiatonicModes.MAJOR),
          mo.mel_cycle_scale(4, tonic=Note("E3"), scale=NS.DiatonicModes.PHRYGIAN)],
         1, 2),
        # multiple part, multiple melodies
        ([ro.p_b__4_note_on__4, ro.p_b__4_note_on__6],
         [mo.mel_cycle_scale(4, Note("C3"), NS.DiatonicModes.MAJOR),
          mo.mel_cycle_scale(6, Note("E3"), NS.DiatonicModes.PHRYGIAN)],
         2, 2),
        # multiple part, mixed sequence (Melody and Note)
        ([ro.p_b__4_note_on__4, ro.p_b__4_note_on__6],
         [mo.mel_cycle_scale(4, tonic=Note("C3"), scale=NS.DiatonicModes.MAJOR),
          Note("C4")],
         2, 2)
    ]
)
def test_melodies_from_melody_sequence(parts, melodies, n_parts, n_melodies):
    sp = TrackBuilder(parts, melodies)

    assert len(sp.parts) == n_parts
    assert len(sp.melodies) == n_melodies


@pytest.mark.parametrize(
    ["parts", "melodies", "error"],
    [  # 2 part, 1 Note-melody
        ([ro.p_m1_m2, ro.p_m1_m3], [Note(60)], ValueError),
        # 1 part, 2 melodies wrong size
        ([ro.p_b__4_note_on__4],
         [mo.mel_cycle_scale(4, tonic=Note("C3"), scale=NS.DiatonicModes.MAJOR),
          mo.mel_cycle_scale(5, tonic=Note("E3"), scale=NS.DiatonicModes.PHRYGIAN)],
         ValueError),
        # 2 part, 2 melodies wrong size
        ([ro.p_b__4_note_on__4, ro.p_b__4_note_on__6],
         [mo.mel_cycle_scale(4, Note("C3"), NS.DiatonicModes.MAJOR),
          mo.mel_cycle_scale(7, Note("E3"), NS.DiatonicModes.PHRYGIAN)],
         ValueError),
        # 2 part, 3 melodies (multi-part should be 1 to 1)
        ([ro.p_b__4_note_on__4, ro.p_b__4_note_on__6],
         [mo.mel_cycle_scale(4, Note("C3"), NS.DiatonicModes.MAJOR),
          mo.mel_cycle_scale(6, Note("E3"), NS.DiatonicModes.PHRYGIAN),
          mo.mel_cycle_scale(6, Note("F3"), NS.DiatonicModes.LYDIAN)],
         ValueError)
    ]
)
def test_melodies_raises(parts, melodies, error):
    with pytest.raises(error):
        sp = TrackBuilder(parts, melodies)

# TODO
@pytest.mark.parametrize(
    ["parts","melodies","n_melodies"],
    [
        # single part, single note
        (None,None),
        # single part, multiple note
        (None,None),
        # single part, single melody
        (None,None),
        # single part, multiple melody
        (None,None),
        # single part, mixed note/melody
        (None,None)
    ]

)
def test_parse_single_part(parts,melodies,n_melodies):
    sp = TrackBuilder(parts=parts, melodies=melodies)

    assert not sp.is_multi_part
    assert len(sp.melodies) == n_melodies




