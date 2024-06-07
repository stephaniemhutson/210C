# 210C

## Setting up a Virtual Environment

How to set up a virtual environment: Start outside of your repository. replace "test_env" with the file path to your repository.

```bash:
mkdir test_env
python3 -m venv ./test_env

# nagivate to the directory
pushd test_env

# activate the virtual environment
test_env %> . bin/activate

(test_env) test_env %> pip list
```
You will have no libraries installed.

```
Package Version
------- -------
pip     24.0
```

install your libraries either individually, or from a `requirements.txt` files that you have put into the top of your repository.
```bash:
(test_env) test_env %>
(test_env) test_env %> pip install -r requirements.txt
Collecting sequence-jacobian (from -r requirements.txt (line 1))
  Using cached sequence_jacobian-1.0.0-py3-none-any.whl.metadata (4.7 kB)
Collecting numpy (from -r requirements.txt (line 2))
  Using cached numpy-1.26.4-cp312-cp312-macosx_11_0_arm64.whl.metadata (61 kB)
Collecting matplotlib (from -r requirements.txt (line 3))
  Downloading matplotlib-3.9.0-cp312-cp312-macosx_11_0_arm64.whl.metadata (11 kB)
...
```

Check pip list again, and you will find that your libraries have been installed.

```bash:
(test_env) test_env %> pip list
Package           Version
----------------- -----------
contourpy         1.2.1
cycler            0.12.1
fonttools         4.53.0
kiwisolver        1.4.5
llvmlite          0.42.0
matplotlib        3.9.0
numba             0.59.1
numpy             1.26.4
packaging         24.0
pillow            10.3.0
pip               24.0
pyparsing         3.1.2
python-dateutil   2.9.0.post0
scipy             1.13.1
sequence-jacobian 1.0.0
six               1.16.0
````



## Problem Set 1

Language: Python

libraries:
* numpy
* scipy
* matplotlib

To Run:

`> python3 ./PS1/problem_set1.py`

Collaborators:
* Grace
* Bridget
* Sondre


## Problem Set 2

Language: Stata

Collaborators:
* Sondre

## Problem Set 3

PDF of hand written answers

## Problem Set 4

Language: Python 3

`pip install -r requirements.txt`

Collaborators:
* Max
