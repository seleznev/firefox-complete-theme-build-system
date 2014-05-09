===================
Directory structure
===================

A required files structure

::

  .
  ├── config.json
  ├── extension
  │   ├── chrome.manifest
  │   └── install.rdf.in
  ├── install.rdf.in
  └── theme
      ├── shared
      ├── chrome-30
      ├── chrome.manifest.in
      ├── install.rdf.in

A real example files structure

::

  .
  ├── config.json
  ├── extension
  │   ├── bootstrap.js
  │   ├── chrome
  │   ├── chrome.manifest
  │   ├── icon.png
  │   ├── include
  │   └── install.rdf.in
  ├── install.rdf.in
  └── theme
      ├── chrome
      │   ├── browser
      │   ├── global
      │   └── symbolic-icons
      ├── chrome-30
      │   └── browser
      │       └── devtools
      ├── chrome-31
      │   ├── browser
      │       └── devtools
      │   └── global
      ├── chrome-32
      │   ├── browser
      │   ├── global
      │   └── mozapps
      ├── chrome.manifest.in
      ├── icon.png
      ├── install.rdf.in
      └── preview.png

