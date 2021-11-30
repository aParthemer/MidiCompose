from dataclasses import dataclass


@dataclass
class DiatonicModes:

    IONIAN = [2, 2, 1, 2, 2, 2, 1]
    DORIAN = [2, 1, 2, 2, 2, 1, 2]
    PHRYGIAN = [1, 2, 2, 2, 1, 2, 2]
    LYDIAN = [2, 2, 2, 1, 2, 2, 1]
    MIXOLYDIAN = [2, 2, 1, 2, 2, 1, 2]
    AEOLIAN = [2, 1, 2, 2, 1, 2, 2]
    LOCRIAN = [1, 2, 2, 1, 2, 2, 2]

    # aliases
    MAJOR = IONIAN
    MINOR = AEOLIAN

@dataclass
class NonDiatonicScales:
    MELODIC_MINOR = [2,1,2,2,2,2,1]
    HARMONIC_MINOR = [2,1,2,2,1,3,1]
    WHOLE_TONE = [2,2,2,2,2,2]
    DIMINISHED_HW = [1,2,1,2,1,2,1,2]
    DIMINISHED_WH = [2,1,2,1,2,1,2,1]
