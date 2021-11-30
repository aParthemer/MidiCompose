from MidiCompose.logic.rhythm.beat import Beat
from MidiCompose.logic.rhythm.measure import Measure
from MidiCompose.logic.rhythm.part import Part

#### BEAT ####

b_111 = Beat([1,1,1])
b_011 = Beat([0,1,1])
b_012 = Beat([0,1,2])
b_211 = Beat([2,1,1])
b_120 = Beat([1,2,0])

b_1111 = Beat([1,1,1,1])
b_1000 = Beat([1,0,0,0])
b_1222 = Beat([1,2,2,2])
b_0111 = Beat([0,1,1,1])
b_0121 = Beat([0,1,2,1])
b_0122 = Beat([0,1,2,2])
b_2111 = Beat([2,1,1,1])
b_2120 = Beat([2,1,2,0])

#### MEASURE ####

m_1000_1222__1 = Measure([b_1000,b_1222])
m_2111_2120__2 = Measure([b_2111,b_2120])
m_0121_1222__3 = Measure([b_0121,b_1222])

#### PART ####
p_m1_m2 = Part([m_1000_1222__1,m_2111_2120__2])
p_m1_m2_n_note_on = p_m1_m2.n_note_on

p_m1_m3 = Part([m_1000_1222__1,m_0121_1222__3])
p_m1_m3_n_note_on = p_m1_m3.n_note_on

p_b__4_note_on__4 = Part([m_1000_1222__1,m_1000_1222__1])
p_b__4_note_on__6 = Part([m_1000_1222__1,
                          m_2111_2120__2,])

