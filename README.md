typeschema
===========

[![Build Status](http://tyba.cc:8080/buildStatus/icon?job=tcard/typeschema)](http://tyba.cc:8080/job/tcard/job/typeschema/) [![online documention](http://b.repl.ca/v1/online-documention-blue.png)](http://tyba:tyb4d0cs@docs.tyba.cc/typeschema/)

Requirements
------------

* persistence == 0.1.0
* typeschema == 0.0.1
* knot == 0.3.0
* slug == 1.0.0
* mock == 1.0.1

Packages
--------

* typeschema

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
    dependency_links=[
        'http://github.com/Tyba/typeschema/tarball/master#egg=typeschema-<version>'
    ],
    install_requires=[
        ...
        'typeschema == <version>',
        ...
    ]
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
