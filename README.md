# EtcAbductionPy

## An implementation of Etcetera Abduction in Python

This software is a reference implementation of Etcetera Abduction. Given a knowledge base of first-order definite clauses and a set of observables, this software identifies the most probable set of assumptions that logically entails the observations, assuming the conditional independence of each assumption. 

For more information, see the project homepage: http://asgordon.github.io/EtcAbductionPy/

## Getting started

Please use `uv` for a modern Python environment and ease-of-use. Installation: [here](https://docs.astral.sh/uv/getting-started/installation/)

```
git clone https://github.com/asgordon/EtcAbductionPy.git
cd EtcAbductionPy
uv run -m etcabductionpy -h
```
