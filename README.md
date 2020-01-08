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

python3 -m venv trends-env; source trends-env/bin/activate
pip install -r requirements.txt

jupyter lab
```

