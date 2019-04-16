# Atlas Trends API demonstration

## Introduction

The Atlas Trends API is an implementation of a novel method to cluster RTT time series using nonparametric Bayesian models. The API allows producing humanlike segmentation of [RIPE Atlas](http://atlas.ripe.net/) RTT time series.

This repository contains the following Python notebooks demonstrating the API usage:

Name | Description | Online Notebook
:----|:------------|:-----------------
Atlas Trends API | Overview of the API | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/maxmouchet/atlas-trends-demo/blob/master/notebooks/Atlas%20Trends%20API.ipynb)

## Getting Started

You can run the notebooks on Google Colab by following the links at the top, or locally by running the following in a terminal:

```bash
git clone https://github.com/maxmouchet/atlas-trends-demo.git
cd atlas-trends-demo
pipenv sync
pipenv run jupyter lab
```

This requires Python 3 and [pipenv](https://pipenv.readthedocs.io/en/latest/), which can be installed using

```bash
pip install --user pipenv # Or pip3 depending on your Python setup
```
