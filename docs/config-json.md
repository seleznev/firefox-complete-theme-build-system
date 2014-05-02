# config.json

## Structure and fuilds

* __version__

  _Required: yes._

  Version of all addons: theme, extension and package. This string will
  preplace `@VERSION@` string in all `install.rdf.in` files.

* __min-version__

  _Required: yes._

  Min support version of Firefox for all addons. Will replace `@MIN_VERSION@`.

* __max-version__

  _Required: yes._

  Max support version of Firefox for all addons. Will replace `@MAX_VERSION@`.

* __xpi__

  _Required: yes._

  Contains file names for all results .xpi files. File name, not path! Also you
  can use `@VERSION@` string in here.

  - __theme__

    _Required: yes._
    
    File name for theme's xpi. For example: `test-theme.xpi`.

  - __extension__

    _Required: yes._
    
    File name for extension's xpi. For example: `test-extension.xpi`.

  - __package__

    _Required: yes._
    
    File name for package's xpi what will contain `install.rdf`, theme and
    extension installer files. For example: `test-@VERSION@.xpi`.

* __directory-structure__

  _Required: no._

  - __shared-dir__

    _Required: no. Default value - `shared`._

    It's contains directory name for shared files in a theme beetwin Firefox
    versions.

## Example

```JSON
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
```
