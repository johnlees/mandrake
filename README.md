# mandrake <img src='docs/images/mandrake.png' align="right" height="139" />

<!-- badges: start -->
[![Build and run tests](https://github.com/johnlees/mandrake/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/johnlees/mandrake/actions/workflows/python-package-conda.yml)
[![Documentation Status](https://readthedocs.org/projects/mandrake/badge/?version=latest)](https://mandrake.readthedocs.io/)
<!-- badges: end -->

Fast visualisation of the population structure of pathogens using Stochastic Cluster Embedding

Documentation available at: https://mandrake.readthedocs.io/en/latest/

## Installation (briefly)

See https://mandrake.readthedocs.io/en/latest/installation.html for more details.

You will need some dependencies, which you can install through `conda`:
```
conda create -n mandrake_env python
conda env update -n mandrake_env --file environment.yml
conda activate mandrake_env
```

You can then clone this repository, and run:
```
python setup.py install
```

### GPU acceleration
You will need the CUDA toolkit installed.

If you have the ability to compile CUDA (e.g. `nvcc`) you should see a message:
```
CUDA found, compiling both GPU and CPU code
```
otherwise only the CPU version will be compiled:
```
CUDA not found, compiling CPU code only
```

## Usage
After installing, an example command would look like this:
```
mandrake --sketches sketchlib.h5 --kNN 500 --cpus 4 --maxIter 1000000
```
This would use a file `sketchlib.h5` created by [pp-sketchlib](https://github.com/johnlees/pp-sketchlib)
to calculate accessory distances using 500 nearest neighbours.

Output can be found in numerous files prefixed `mandrake.embedding*`.

Other useful arguments include:

- `--alignment` use a fasta alignment to calculate distances
- `--accessory` use a presence/absence file (Rtab or similar) to calculate distances
- `--distances` use a `.npz` file from a previous run and skip straight to the embedding step
- `--labels` give labels to colour the output by
- `--perplexity` change the perplexity of the preprocessing (similar to t-SNE)
- `--animate` produce a video of the optimisation
- `--use-gpu` use a GPU for the run. Make sure to increase `--n-workers`.

See the [documentation](https://mandrake.readthedocs.io/en/latest/) for more details.
