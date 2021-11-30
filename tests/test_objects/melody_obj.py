from icecream import ic as ice

from MidiCompose.logic.harmony.note import Note

from MidiCompose.logic.melody.melody import Melody
from MidiCompose.logic.melody.note_set import NoteSet
from MidiCompose.logic.melody import NOTE_SETS

#### MELODY GENERATOR FUNCTIONS ####

def mel_cycle_scale(n_notes: int, tonic: Note, scale: list) -> Melody:
    """
    Cycles up and down C major scale for arbitrary number of notes.
    """
    ns = NoteSet()

    scale_asc = ns.from_scale(tonic=tonic,scale=scale)

    scale_desc = scale_asc[1:-1]
    scale_desc.reverse()

    scale_cycle = scale_asc + scale_desc

    n = 0
    notes = []
    while n < n_notes:
        for note in scale_cycle:
            if n >= n_notes:
                break
            else:
                notes.append(note)
                n += 1

    melody = Melody(notes)

    return melody


#### MELODY-LIKE OBJECTS ####

mel_like_60_62_64 = [Note(60),Note(62),Note(64)]
mel_60_62_64 = Melody(mel_like_60_62_64)

