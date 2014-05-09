===========
config.json
===========

Main config for all addons.

Structure and fuilds
====================

* **version**

  *Required: yes.*

  Version of all addons: theme, extension and package. This string will
  preplace ``@VERSION@`` string in all ``install.rdf.in`` files.

* **min-version**

  *Required: yes.*

  Min support version of Firefox for all addons. Will replace ``@MIN_VERSION@``.

* **max-version**

  *Required: yes.*

  Max support version of Firefox for all addons. Will replace ``@MAX_VERSION@``.

* **xpi**

  *Required: yes.*

  Contains file names for all results .xpi files. File name only, not path!
  Also you can use ``@VERSION@`` string in here.

  - **theme**

    *Required: yes.*
    
    File name for theme's xpi. For example: ``test-theme.xpi``.

  - **extension**

    *Required: yes.*
    
    File name for extension's xpi. For example: ``test-extension.xpi``.

  - **package**

    *Required: yes.*
    
    File name for package's xpi what will contain ``install.rdf``, theme and
    extension installer files. For example: ``test-@VERSION@.xpi``.

* **directory-structure**

  *Required: no.*

  - **shared-dir**

    *Required: no. Default value -* ``shared``.

    It's contains directory name for shared files in a theme beetwin Firefox
    versions.

Example
=======

::

  {
    "version": "0.1",
    "min-version": "30.0",
    "max-version": "33.0a1",
    "xpi": {
      "theme": "firefox-theme-test.xpi",
      "extension": "firefox-extension-test.xpi",
      "package": "firefox-all-in-one-@VERSION@.xpi"
    },
    "directory-structure": {
      "shared-dir": "chrome"
    }
  }

