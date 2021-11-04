from dataclasses import dataclass
from typing import Collection, Union

import numpy as np
from icecream import ic
from mido import MidiFile,MidiTrack,Message,MetaMessage

import config
import parse_state as ps

#### OBJECTS ####


#### MESSAGE PROTOCOLS ####

# TODO
def ofn(time,off_note=64,on_note=64,channel=0,velocity=80):
    """
    ofn "off on" is used when simultaneously sending "note_off" and "note_on" messages.
    eg]
        [...,
         Message(type="note_off",note=<off_note>,time=<time>),
         Message(type="note_on",note=<on_note>,time=0))
         ...]
    """
    _ofn = [Message(type="note_off",note=off_note,channel=channel,time=time),
           Message(type="note_on",note=on_note,channel=channel,velocity=velocity,time=0)]
    return _ofn

#### FROM STATE ####


#### TRACK ####

def track_from_messages(messages: Collection[Message]) -> MidiTrack:
    return MidiTrack(messages)

#### FILE ####

def mid_from_tracks(tracks: Collection[MidiTrack],
                    tpb: int = 480) -> MidiFile:
    mid = MidiFile()
    mid.ticks_per_beat = tpb
    [mid.tracks.append(t) for t in tracks]
    return mid


def save_mid(mid: MidiFile,
             path: str) -> None:
    mid.save(path)

# abs_state_bin = ps.get_abs_state_bin()

if __name__ == '__main__':

    STATE = np.array([-1,
             -2,
             -3, 3, 0,1,1,
             -3, 3, 0,1,2,
             -3, 3, 0,1,1,
             -2,
             -3, 4, 1,2,1,2,
             -3, 4, 1,2,1,1,
             -3, 4, 1,1,0,0,
             -1])
    state_a = np.array(
        [-1,
         -3, 4,
         1, 1, 1, 1,
         -3, 3,
         1, 1, 1,
         -3, 5,
         1, 2, 1, 1, 1,
         -3, 4,
         1, 0, 1, 0,
         -1]
    )
    TPB = 60

    sa = ps.get_state_attributes(state=STATE,tpb=TPB)
    ic(sa.sub_flags,
       sa.total_ticks,
       sa.active_state,
       sa.abs_timestamp,
       sa.active_state_comp,
       sa.timedelta,
       sa.abs_timestamp_comp,
       sa.msg_types,
       )

    m = get_messages(sa.msg_types,sa.timedelta,64)
    ic(m)
    t = track_from_messages(m)
    ic(t)
    mid = mid_from_tracks([t], 60)
    ic(mid)

    p = config.DIR_MIDIFILES
    save_mid(mid,p + "gdf.mid")



