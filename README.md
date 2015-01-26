typeschema [![image](https://readthedocs.org/projects/typeschema/badge/?version=latest)](http://typeschema.readthedocs.org/) [![Build Status](https://travis-ci.org/tyba/typeschema.svg)](https://travis-ci.org/tyba/typeschema)
===========

Packages
--------

* typeschema
* typeschema.decorators
* typeschema.types.time
* typeschema.types.location
* typeschema.properties
* typeschema.properties.time
* typeschema.properties.location

Compatibility
-------------

This library is developed and tested for Python 2.7. It is not compatible with Python 3 at the moment.

Installation
------------

### From PyPI

```sh
pip install typeschema
```

### Development mode

Clone this repository, `cd` to it, and then:

```sh
pip install -e .
```

Makes the package available on `sys.path` symlinked so that it can be edited directly from 
its source checkout.

Caveats: If any other package install this one as dependency the link will be
removed, and the command must be executed again.

### Production mode
```sh
sudo pip install .
```

### As a dependency
At your setup.py add:
```python
setup(
    ...
    install_requires=[
        ...
        'typeschema==<version>'
        ...
    ]
)
```

Documentation
-------------


```sh
cd docs
sudo pip install -r requirements.txt
sphinx-build -b html . build
```

After running those commands, the documention can be find at docs/build/index.html.


Tests
-----

Tests are in the `tests` folder.
Run them with `nosetests` or `py.test`.
