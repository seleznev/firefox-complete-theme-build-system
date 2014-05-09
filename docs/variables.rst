=========
Variables
=========

Predefined variables that can be used in .css files.

* APP_VERSION

  The value gets from name of current processing "chrome" directory. For
  example, in "chrome-30" this variable will be defined as "30".

  It's most useful for code in the shared directory.

  ::

     %if APP_VERSION == 30
     /* Code for Firefox 30 */
     %else
     /* Code for Firefox 31 and later */
     %endif

