# Wagtail References [![Build Status](https://travis-ci.com/thclark/wagtail_references.svg?branch=master)](https://travis-ci.com/thclark/wagtail_references)

BibTeX based  bibliography 

## Templates

**"But, where are the templates?!"** is a natural question. Answer: There aren't any templates or tags so far...
I run all my wagtail installations in headless mode with a react front end, so can only justify putting in place the
templates for managing the references on wagtail.
If you'd like to do so, I'm very open to collaboration :)

I might get around to adding some templates for the listings shown in wagtail, as they're currently pretty ugly (showing
 the raw BibTeX) but will see if this project gets some traction and user first.
  
## Displaying references on the front end

I recommend [bibtex-js](https://github.com/pcooksey/bibtex-js) for parsing and displaying the bibtex on your front end.
  
## Requirements

Wagtail References is tested on Django 2.1 or later and Wagtail 2.3 or later.

## Supported Versions

Python: 3.6

Django: 2.1

Wagtail: 2.3

## Getting started

Installing from pip:

```
pip install wagtail_references
```

Adding to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'wagtail_references',
    ...
]
```

Running the migrations:

```
python manage.py migrate wagtail_references
```

## Reference Model

There's only one database model ``Reference``, which is registered as a snippet in Wagtail, making it searchable and
selectable. The model has a (required) ``slug`` field which is automatically set by signal handlers which extract and normalise the reference key.

For example, if you have the following bibtex entry:
```
@article{Clark2017a,
author = {Clark, Thomas H. E. and Lueck, Rolf G. and Hay, Alex E. and Davey, Thomas and Stern, Peter and Horwitz, Rachel and Pearson, Nicola},
journal = {Proc. of the 12th European Wave and Tidal Energy Conference},
pages = {7},
title = {{InSTREAM : Measurement , Characterisation and Simulation of Turbulence from Test Tank to Ocean .}},
year = {2017}
}
``` 
the slug will automatically be set to clark2017a. Duplicate slugs are not valid, which is how we maintain uniqueness
across all the references added to the CMS.

## Examples

For your and our testing purposes, it's useful to have some examples to hand, so I've prepared some in the ``examples.py`` file, which simply contains a series of different bibtex references.

If you encounter awkward references or ones which won't validate, please post them into a github issue so I can help diagnose and add them for test.
