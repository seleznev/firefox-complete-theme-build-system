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

## Copyright

Following files was created by Mozilla:

* src/build/makeutil.py

* src/build/preprocessor.py

* docs/preprocessor.rst
