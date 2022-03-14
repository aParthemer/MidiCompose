import pytest
from MidiCompose.logic.harmony.key import KeySchema

@pytest.mark.parametrize(
    argnames=["value","expected"],
    argvalues=[
        ("major",KeySchema["MAJOR"]),
        ("MAJOR",KeySchema["MAJOR"]),
        (KeySchema["MINOR"],KeySchema["MINOR"])
    ]
)
def test_parse(value,expected):
    try:
        ks = KeySchema(value)
    except:
        try:
            ks = KeySchema.parse(value)
        except:
            raise

    assert ks == expected