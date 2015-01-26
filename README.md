typeschem [![image](https://readthedocs.org/projects/typeschema/badge/?version=latest)](http://typeschema.readthedocs.org/) [![Build Status](https://travis-ci.org/Tyba/typeschema.svg)](https://travis-ci.org/Tyba/typeschema)
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

Installation
------------

### Development mode
```sh
sudo pip install -e .
```

Makes the package available on sys.path, but can still be edited directly from 
its source checkout, thanks to a link.

Caveats: If any other package install this one as dependency the link will be
removed. And the command must be executed again.

### Production mode
```sh
sudo pip install .
```

### As a dependency
At your setup.py add:
```python
setup(
    ...
    install_requires=dependency_links([
        ...
        'http://github.com/Tyba/typeschema/tarball/master#egg=typeschema==<version>'
        ...
    ])
)
```

Documentation
-------------


```sh
cd docs
sudo pip install -r requirements.txt
sphinx-build -b html . build
```

After run this commands, the documention can be find at docs/build/index.html


Tests
-----

Tests are in the `tests` folder.
To run them, you need `nosetests` or `py.test`.
