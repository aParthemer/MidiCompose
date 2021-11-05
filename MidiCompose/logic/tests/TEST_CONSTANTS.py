import numpy as np
import pytest
from MidiCompose.logic.rhythm import Beat,Measure

#### MEASURE OBJECTS ####

m1 = Measure([Beat(4),Beat(4)])
m1_st = np.array([-2,
                  -3,4,0,0,0,0,
                  -3,4,0,0,0,0])

