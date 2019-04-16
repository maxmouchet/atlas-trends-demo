import datetime as dt

import numpy as np
import pandas as pd
import pytz


def to_dataframe(obj, skip_na=True):
    df = pd.DataFrame.from_records(
        obj['results'],
        columns=obj['metadata']['schema']
    )
    df['dt'] = df.timestamp.apply(lambda x: dt.datetime.fromtimestamp(x, pytz.UTC))
    df.loc[df.status != 0, 'rtt'] = np.nan
    df.set_index('dt', inplace=True)
    if skip_na:
        df = df[df.rtt.first_valid_index():]
    return df


def get_segments(df):
    segments = []
    last_idx, last_state = 0, df.state[0]
    for i in range(1, len(df.state)):
        if (df.state[i] != df.state[i-1]) or (i == len(df.state)-1):
            segments.append({
                'start': last_idx,
                'stop': i,
                'state': last_state
            })
            last_idx, last_state = i, df.state[i]
    return segments


def compute_transition_matrix(seq):
    mapping = {x[1]: x[0] for x in enumerate(sorted(np.unique(seq)))}
    transmat = np.zeros((len(mapping), len(mapping)))
    for i in range(len(seq)-1):
        transmat[mapping[seq[i]], mapping[seq[i+1]]] += 1
    transmat = transmat / np.sum(transmat, axis=1)[:, np.newaxis]
    return mapping, transmat


def utc_datetime(*args):
    return dt.datetime(*args, tzinfo=pytz.UTC)


def td_format(td_object):
    """
    Python format timedelta to string
    https://stackoverflow.com/a/13756038
    """
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60),
        # ('second',      1)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)
