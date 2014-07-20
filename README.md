# Firefox Complete Theme Build System

Scripts pack that can help you to make a Firefox theme.

## How to use

Main script is __make-xpi.py__ written on Python 3. Use it to build xpi and clean temporary files.

```Bash
$ ./make-xpi.py [TARGET]
```

or

```Bash
$ python3 make-xpi.py [TARGET]
```

Available targets: _all_, _theme_, _extension_ and _clean_. Default is _all_.

Examples:

```Bash
$ ./make-xpi.py
$ ./make-xpi.py all
$ ./make-xpi.py theme
$ ./make-xpi.py extension
$ ./make-xpi.py clean
```

Also you can specifity _$VERSION_ environment variable or use _--version_ to override you value in _config.json_.

```Bash
$ ./make-xpi.py --version="0.9" all
$ VERSION="0.9" ./make-xpi.py all
```

For more details try _--help_.

```Bash
$ ./make-xpi.py --help
```

## Build environment

You need Python 2 and Python 3 in your system's $PATH. For example:

```Bash
$ python2 --version
Python 2.7.8
$ python3 --version
Python 3.4.1
```

For override path to python2 you can use $PYTHON2PATH variable, to python3:

```Bash
$ /your/path/to/python3 make-xpi.py
```

## Copyright

Following files was created by Mozilla:

* src/build/makeutil.py

* src/build/preprocessor.py

* docs/preprocessor.rst
