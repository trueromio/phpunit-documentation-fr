# PHPUnit Documentation with Sphinx

The goal of this project is to come up with a proof-of-concept
for migrating PHPUnit's documentation from DocBook XML to
reStructuredText in order to achieve:

- an more streamlined process for contributing to the documentation
- better support for translations
- an easier build process

As this is a work in progress, the repository only contains the
documentation for PHPUnit 6.1.

## Converting DocBook XML to ReStructuredText

### Requirements

- Python

Running the `conversion/DocBookToReST` Bash script will take all XML files from
`docbook/`, convert them to `.rst` files with the help of
`DocBookToReST.py` and write them to `source/`.

### Tests

Run tests by executing command `python tests/conversion.py`

## Building the HTML Documentation

### Requirements

- Python
- [Sphinx](http://www.sphinx-doc.org/)
- [Read the Docs Sphinx Theme](https://github.com/rtfd/sphinx_rtd_theme)

To build the complete documentation run:

    make html

Afterwards you will find the HTML files in `build/html`.
