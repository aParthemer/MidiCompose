from dataclasses import dataclass
from typing import List

import numpy as np
from icecream import ic

import config
from MidiCompose.translation import parse_state as ps
from MidiCompose.translation.parse_state import StateAttributes


#### ATTRIBUTE CONTAINERS ####

@dataclass
class AdjustedAttributes:
    adj_timestamp: np.ndarray
    adj_msg_types: np.ndarray

@dataclass
class ConsolidatedAttributes:
    cons_timestamp: np.ndarray
    cons_timedelta: np.ndarray
    total_ticks: int
    ticks_per_beat: int

@dataclass
class ParallelAttributes:
    """
    Container used for generating midi from parallel state.
    """
    cons_attributes: ConsolidatedAttributes
    adj_attributes: List[AdjustedAttributes]


#### FILL ATTRIBUTE CONTAINERS ####

def _get_consolidated_attrs(state_attrs: List[StateAttributes]) -> ConsolidatedAttributes:

    # get consolidated absolute timestamps
    cons_timestamp = ps.get_cons_abs_ts_comp([sa.timestamp_comp for sa in state_attrs])
    # get consolidated timedelta
    cons_timedelta = ps.get_timedelta(cons_timestamp)

    total_ticks = []
    tpb = []
    for sa in state_attrs:
        total_ticks.append(sa.total_ticks)
        tpb.append(sa.ticks_per_beat)

    # total_ticks must be uniform
    if len(set(total_ticks)) != 1:
        msg = f"All child `states` must contain the same `total_ticks`."
        raise Exception(msg)
    else:
        total_ticks = total_ticks[0]

    # ticks_per_beat must be uniform
    if len(set(tpb)) != 1:
        msg = f"All child `states` must have the same `ticks_per_beat`."
        raise Exception(msg)
    else:
        tpb = tpb[0]

    return ConsolidatedAttributes(cons_timestamp=cons_timestamp,
                                  cons_timedelta=cons_timedelta,
                                  total_ticks=total_ticks,
                                  ticks_per_beat=tpb)

def _get_adjusted_attrs(state_attrs: List[StateAttributes],
                        cons_attrs: ConsolidatedAttributes) -> List[AdjustedAttributes]:

    adjusted_attrs = list()

    # adjust active_state, msg_type, etc to match consolidated time by comparing absolute timestamps
    for sa in state_attrs:

        # boolean mask to match indeces of individual states with consolidated timestamps
        mask_ts_in_cons = np.in1d(cons_attrs.cons_timestamp,
                                  sa.timestamp_comp)

        # adjusted absolute timestamp
        adj_abs_ts_comp = np.where(mask_ts_in_cons,
                                   cons_attrs.cons_timestamp,
                                   -4)
        # adjusted msg type
        adj_msg_types = np.full(shape=cons_attrs.cons_timestamp.shape,
                                fill_value="-4",
                                dtype=object)
        idx_adj = np.where(adj_abs_ts_comp != -4)
        adj_msg_types[idx_adj] = sa.msg_types

        adj_attrs = AdjustedAttributes(adj_timestamp=adj_abs_ts_comp,
                                       adj_msg_types=adj_msg_types)

        adjusted_attrs.append(adj_attrs)

    return adjusted_attrs

def _get_parallel_attrs(cons_attrs: ConsolidatedAttributes,
                        adj_attrs: List[AdjustedAttributes]) -> ParallelAttributes:
    return ParallelAttributes(cons_attrs,
                              adj_attrs)

#### MAIN ####

def get_parallel_attrs(state_attrs: List[StateAttributes]):

    cons_attrs = _get_consolidated_attrs(state_attrs)
    adj_attrs = _get_adjusted_attrs(state_attrs, cons_attrs)

    return _get_parallel_attrs(cons_attrs, adj_attrs)






