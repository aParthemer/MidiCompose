from icecream import ic as ice

from MidiCompose.logic.harmony.note import Note

from MidiCompose.logic.melody.melody import Melody
from MidiCompose.logic.melody.note_set import NoteSet
from MidiCompose.logic.melody import scale

#### MELODY-LIKE OBJECTS ####

mel_like_60_62_64 = [Note(60),Note(62),Note(64)]
mel_60_62_64 = Melody(mel_like_60_62_64)

