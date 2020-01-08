import datetime as dt
import math
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pytz
import seaborn as sns
from matplotlib.dates import DateFormatter, HourLocator
from pandas.plotting import register_matplotlib_converters
from scipy.stats import gaussian_kde

from .utils import *

register_matplotlib_converters()


def set_mpl_style(font_size=12):
    # Old seaborn versions (such as the one in Google Colab)
    # modify the default matplotlib style on import.
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        sns.reset_orig()

    plt.rc('figure', figsize=(18, 2.5))
    plt.rc('font', size=font_size)
    plt.rc('axes', titlesize=font_size)
    plt.rc('text', usetex=False)
    plt.rc('font', family='sans-serif')
    plt.rc('legend', frameon=False)


def plot_trends(df, legend=True, ax=None):
    if ax is None:
        ax = plt.gca()
    if 'rtt' in df:
        plot_rtt(df, ax=ax)
    if 'state' in df:
        plot_state(df, ax=ax)
    if legend:
        add_legend(df, ax=ax)


def plot_rtt(df, ax=None):
    if ax is None:
        ax = plt.gca()
    ax.plot(df.index, df.rtt, drawstyle='steps-mid', lw=1)
    ax.set_xlim(df.index.min(), df.index.max()+dt.timedelta(minutes=4))
    ax.set_ylabel('RTT (ms)')
    ax.xaxis.set_major_locator(HourLocator(byhour=0, tz=pytz.UTC))
    ax.xaxis.set_major_formatter(DateFormatter('%d %b', tz=pytz.UTC))


def plot_state(df, ax=None):
    if ax is None:
        ax = plt.gca()
    palette = sns.husl_palette(df.state.max(), l=0.7, s=.9)
    for segment in get_segments(df):
        start_dt = df.index[segment['start']]
        stop_dt = df.index[segment['stop']]
        color = palette[segment['state']-1]
        ax.axvspan(start_dt, stop_dt, alpha=0.3, color=color)


def add_legend(df, ax=None):
    if ax is None:
        ax = plt.gca()

    Δt = (df.index[1:] - df.index[:-1]).mean() / np.timedelta64(1, 's')
    mapping, transmat = compute_transition_matrix(df.state)

    palette = sns.husl_palette(df.state.max(), l=0.7, s=.9)
    artists, labels = [], []

    for state in sorted(df.state.unique()):
        # Ignore division by zero (handled later)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            avg_duration = (
                1 / (1 - transmat[mapping[state], mapping[state]])) * Δt

        if avg_duration == math.inf:
            avg_duration_str = '∞'
        else:
            avg_duration_str = td_format(dt.timedelta(seconds=avg_duration))

        artists.append(plt.Rectangle(
            (0, 0), 1, 1, color=palette[state-1], alpha=0.6))
        labels.append('State {}\nAvg. duration\n{}'.format(
            state, avg_duration_str))

    ax.legend(artists, labels, bbox_to_anchor=(
        0.5, -0.35), ncol=len(artists), loc='center')


def plot_kde(df, states=None):
    if states is None:
        states = df.state.unique()

    xmin, xmax = df.rtt.min(), df.rtt.max()
    X = np.arange(xmin-10, xmax+10, 0.1)
    palette = sns.husl_palette(df.state.max(), l=0.7, s=.9)

    for state in sorted(states):
        obs = df[df.state == state].rtt.dropna()
        if len(obs) < 1:
            continue
        w = len(obs) / len(df.rtt.dropna())
        pdf = w * gaussian_kde(obs)(X)
        plt.plot(X, pdf, color=palette[state-1])
        plt.fill_between(
            X, pdf, color=palette[state-1], alpha=0.2, label='State {}'.format(state))

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xlim(min(X), max(X))
    plt.xlabel('RTT (ms)')
    plt.ylabel('Density estimation')
    plt.legend(frameon=0)
