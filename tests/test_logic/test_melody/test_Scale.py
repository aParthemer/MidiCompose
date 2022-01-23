from MidiCompose.objects import Scale, Note

params = [
    (Note("C2"), "MAJOR",
     [Note("C2"), Note("D2"), Note("E2"),
      Note("F2"), Note("G2"), Note("A2"),
      Note("B2")])
]

def test_constructor():
    scale = Scale(tonic=Note("C2"), mode="MAJOR")

