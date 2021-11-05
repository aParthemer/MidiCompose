from dataclasses import dataclass
from typing import List, Collection, Union

import numpy as np
from icecream import ic

from mido import Message, MidiTrack, MetaMessage, MidiFile

import config


#### CONTAINER OBJECTS ####

@dataclass
class StateAttributes:
    active_state: np.ndarray
    total_ticks: int
    ticks_per_beat: int

    sub_flags: np.ndarray
    ticks_per_sub: np.ndarray
    timestamp: np.ndarray

    active_state_comp: np.ndarray
    timestamp_comp: np.ndarray
    timedelta: np.ndarray
    msg_types: np.ndarray


#### DEPENDENCE: 0 ####

def get_active_state(state: np.ndarray) -> np.ndarray:
    """
    Returns only elements from state which have to do with activation.
    (ie: {0,1,2}
    """
    idx_active_arr = np.where((state == 0) | (state == 1) | (state == 2))
    active_state = state[idx_active_arr]

    return active_state


def get_subdivision_flags(state: np.ndarray) -> np.ndarray:
    """
    Returns array where each element represents the number of subdivisions within a beat.
    """

    idx_sub_flag = np.where(state == -3)[0] + 1
    sub_flags = np.take(state, idx_sub_flag)

    return sub_flags


#### DEPENDENCE: 1 ####

def get_ticks_per_sub(sub_flags: np.ndarray,
                      tpb: int):
    """
    Returns a 1d array where each element represents the number of ticks in that
    particular subdivision.

    PARAMETERS DEPEND ON:
        - get_subdivision_flags()
    """

    # get ticks per sub
    tick_values = tpb // sub_flags
    ticks_per_sub = np.repeat(tick_values, sub_flags)

    return ticks_per_sub


def get_size_of_active_state(active_st: np.ndarray):
    return active_st.size


def get_active_state_comp(active_st: np.ndarray) -> np.ndarray:
    """
    Strips all "sustain" (2) instances from buffered state so that there's a one-to-one
    relationship between state and time attributes.
    """
    return active_st[active_st != 2]


#### DEPENDENCE: 2 ####

def get_total_ticks(ticks_per_sub: np.ndarray) -> int:
    """
    Returns total number of ticks in State.
    """
    return ticks_per_sub.sum(dtype=int)


def get_timestamp(active_st: np.ndarray,
                  ticks_per_sub: np.ndarray):
    """
    Get the array which represents the absolute time for each TimeUnit in a midi-state.
    """
    size_st = active_st.size

    # initialize empty array of size n+1 compared to active state
    abs_time = np.zeros(shape=(size_st + 1,), dtype=int)
    abs_time[1:] = np.cumsum(ticks_per_sub)

    return abs_time


def get_timestamp_comp(active_st: np.ndarray,
                       timestamp: np.ndarray):
    idx_active_st_comp = np.where((active_st == 1) | (active_st == 0))
    timestamp_comp = timestamp[:-1][idx_active_st_comp]
    return timestamp_comp


def get_msg_types(active_st_comp: np.ndarray):
    asc = active_st_comp

    idx_off = np.where(asc == 0)[0]
    idx_on = np.where(asc == 1)[0]

    # get idx ofn
    idx_elements_equal = np.where(asc[1:] == asc[:-1])[0] + 1
    idx_ofn = np.intersect1d(idx_on, idx_elements_equal)

    msg_types = np.empty(shape=asc.shape, dtype=object)
    msg_types[idx_on] = "note_on"
    msg_types[idx_off] = "note_off"
    msg_types[idx_ofn] = "ofn"

    return msg_types


#### DEPENDENCE: 3 ####

def get_timedelta(timestamp_comp: np.ndarray):
    timedelta = np.zeros(shape=timestamp_comp.shape, dtype=int)
    timedelta[1:] = timestamp_comp[1:] - timestamp_comp[:-1]

    return timedelta


def get_state_attributes(state: np.ndarray,
                         tpb: int) -> StateAttributes:
    """

    """
    active_state = get_active_state(state=state)
    ticks_per_beat = tpb
    sub_flags = get_subdivision_flags(state=state)

    ticks_per_sub = get_ticks_per_sub(sub_flags=sub_flags,
                                      tpb=tpb)
    total_ticks = get_total_ticks(ticks_per_sub=ticks_per_sub)

    timestamp = get_timestamp(active_st=active_state,
                              ticks_per_sub=ticks_per_sub)

    active_state_comp = get_active_state_comp(active_st=active_state)
    timestamp_comp = get_timestamp_comp(active_st=active_state,
                                        timestamp=timestamp)
    timedelta = get_timedelta(timestamp_comp=timestamp_comp)
    msg_types = get_msg_types(active_st_comp=active_state_comp)

    state_attributes = StateAttributes(
        active_state=active_state,
        sub_flags=sub_flags,
        ticks_per_sub=ticks_per_sub,
        total_ticks=total_ticks,
        timestamp=timestamp,
        active_state_comp=active_state_comp,
        timestamp_comp=timestamp_comp,
        timedelta=timedelta,
        msg_types=msg_types,
        ticks_per_beat=ticks_per_beat
    )

    return state_attributes


#### MULTIPLE STATE ####

def get_multiple_state_attributes(states: Collection[np.ndarray],
                                  tpb: int) -> List[StateAttributes]:

    return [get_state_attributes(s, tpb) for s in states]


def get_cons_abs_ts_comp(abs_times: Collection[np.ndarray]):
    """
    Given 2 or more abs_time arrays, return consolidated array.

    Used for mapping parallel states into a single track.
    """

    consolidated = np.zeros(shape=(1,), dtype=int)
    for _abs in abs_times:
        consolidated = np.union1d(_abs, consolidated, )

    return consolidated
