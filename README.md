# documentate
A python package that generates documentation for python packages and modules

WORK IN PROGRESS, NOT WORKING AS INTENDED YET.

# Installation

```pip install -r requirements.txt```

The only dependency is Jinja2.

# Run

```python documentate -i <input directory> -o <output directory>```

# Output
documentate generates a number of html pages which are dependant on the template used.
The html pages will contain documentation automatically generated based on your modules ast.
Please use docstrings and typehints to make the documentation more useful.
