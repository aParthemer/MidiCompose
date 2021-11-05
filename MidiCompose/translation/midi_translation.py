from dataclasses import dataclass
from typing import Collection, Union, List

import numpy as np
from icecream import ic
from mido import MidiFile, MidiTrack, Message, MetaMessage

import config
from MidiCompose.translation import parse_state as ps
from MidiCompose.translation.parse_state import StateAttributes
from MidiCompose.translation.parallel_translation import ParallelAttributes


#### OBJECTS ####


#### MESSAGE PROTOCOLS ####

def ofn(time, off_note=64, on_note=64, channel=0, velocity=80):
    """
    ofn "off on" is used when simultaneously sending "note_off" and "note_on" messages.
    eg]
        [...,
         Message(type="note_off",note=<off_note>,time=<time>),
         Message(type="note_on",note=<on_note>,time=0))
         ...]
    """
    _ofn = [Message(type="note_off", note=off_note, channel=channel, time=time),
            Message(type="note_on", note=on_note, channel=channel, velocity=velocity, time=0)]
    return _ofn


#### FROM STATE ####
def get_messages_from_state(state_attrs: StateAttributes) -> List[Message]:

    # unpack needed attributes
    sa = state_attrs
    timedelta = sa.timedelta
    msg_types = sa.msg_types
    total_ticks = sa.total_ticks
    ic(msg_types,timedelta)

    # TEMPORARY PLACEHOLDERS
    _NOTE = 60
    _CHANNEL = 0
    _VELOCITY = 70

    messages = []
    for i,_time in enumerate(timedelta):
        _type = msg_types[i]
        if _type == "ofn":
            messages.extend(ofn(time=_time,on_note=_NOTE,off_note=_NOTE,
                                channel=_CHANNEL,velocity=_VELOCITY))
        else:
            messages.append(Message(type=_type,time=_time,note=_NOTE,
                                    velocity=_VELOCITY,channel=_CHANNEL))

    _time_last = total_ticks - np.sum(timedelta)
    messages.append(Message(type="note_off",time=_time_last))

    return messages

#### FROM PARALLEL STATE ####

# TODO : break this up
def get_messages_from_parallel_states(par_attrs: ParallelAttributes) -> List[Message]:
    # unpack consolidated attributes
    tpb = par_attrs.cons_attributes.ticks_per_beat
    total_ticks = par_attrs.cons_attributes.total_ticks
    cons_timestamp = par_attrs.cons_attributes.cons_timestamp
    cons_timedelta = par_attrs.cons_attributes.cons_timedelta

    # TEMPORARY: channel/note flags from number of states
    adj_attrs = par_attrs.adj_attributes
    _NOTE = {}
    _CHANNEL = {}
    _VELOCITY = {}
    for i in range(len(adj_attrs)):
        _NOTE[i] = 60 + i * 4
        _CHANNEL[i] = 0 + i
        _VELOCITY[i] = 70

    # get messages
    messages = []
    for i, timedelta in enumerate(cons_timedelta):

        timedelta_used = False
        ic(i, timedelta, timedelta_used)

        for j, adj in enumerate(adj_attrs):

            # handle concurrent messages
            if timedelta_used:
                _time = 0
            else:
                _time = timedelta

            # parse message types
            _type = adj.adj_msg_types[i]
            ic(_type, j)
            if _type == "-4":
                ic("-4")

            elif _type == "ofn":
                messages.extend(ofn(time=_time,
                                    off_note=_NOTE[j], on_note=_NOTE[j],
                                    channel=_CHANNEL[j], velocity=_VELOCITY[j]))
                timedelta_used = True

            elif _type in {"note_on", "note_off"}:
                ic("on/off")
                messages.append(Message(type=_type, time=timedelta, note=_NOTE[j],
                                        channel=_CHANNEL[j], velocity=_VELOCITY[j]))
                timedelta_used = True

    # send final "note_off" message
    remaining_ticks = total_ticks - np.sum(cons_timedelta)
    messages.append(Message(type="note_off", time=remaining_ticks))

    return messages


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

