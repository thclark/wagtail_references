# Wagtail References [![Build Status](https://travis-ci.com/thclark/wagtail_references.svg?branch=master)](https://travis-ci.com/thclark/wagtail_references)

BibTeX based bibliography entries, as wagtail snippets


## Templates

**"But, where are the templates?!"** is a natural question. Answer: There aren't any templates or tags so far...
I run all my wagtail installations in headless mode with a react front end, so can only justify putting in place the
templates for managing the references on wagtail.

If you'd like to do so, I'm very open to collaboration :)

I might get around to adding some templates for the listings shown in wagtail, as they're currently pretty ugly (showing
 the raw BibTeX) but will see if this project gets some traction and users first. **Bottom line: Star this repo on Github
 , so I know you're reading this and interested!** 


## Displaying references on the front end

I recommend [bibtex-js](https://github.com/digitalheir/bibtex-js) for parsing and displaying the bibtex on your front end. 
It doesn't convert tex strings, so you'll want to ensure the `WAGTAILREFERENCES_ENSURE_UNICODE` setting is True.  


## Roadmap

I'd like to include:
- A better snippet editor, possibly using a json editor component and allowing the user to switch between tex and json
- Improved listings template in wagtail
- A `ListSerializer` for serializing out multiple references as a bibjson collection
- A matching react component library for the front end (front end offerings are a hassle)
- An HTML renderer and viewset 


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
selectable. 

### Slugs 

The model has a (required, unique) ``slug`` field which is automatically set from bibtex contents when a reference
is added.

For example, if you have the following bibtex entry:
```
@article{Clark2017a,
author = {Clark, Thomas H. E. and Lueck, Rolf G. and Hay, Alex E. and Davey, Thomas and Stern, Peter and Horwitz, Rachel},
journal = {Proc. of the 12th European Wave and Tidal Energy Conference},
pages = {7},
title = {{InSTREAM : Measurement , Characterisation and Simulation of Turbulence from Test Tank to Ocean .}},
year = {2017}
}
``` 
the slug will automatically be set to ``clark-lueck-hay-davey-stern-horwitz-2017``, with an appended ``-2``, ``-3`` etc
to maintain uniqueness.

The citation key for the bibtex entry will be updated to correspond:
```
@article{clark-lueck-hay-davey-stern-horwitz-2017,
author = ... etc etc ...
}
``` 

Uniqueness is enforced at form validation and database level. Slugs may be edited manually after creation of a reference.

### bibtex and bibjson

The reference model comprises both a `bibtex` field (containing the bibtex string, raw) and a `bibjson` field. 
*Yes, I know this is duplication of data. But I'd rather do that than incur the cost of re-parsing the data every time I
want to serialize it out in a different form. I could've chosen to cache it, but then I don't know how much memory you 
folks have, and don't want to screw your cache if you're managing a lot of references). It was a judgement call. 
Use-case and an alternative solution? File an issue.*

The `bibjson` is stored natively as JSON if you have POSTGRES, otherwise as a string (thanks to [`django-jsonfield`](https://github.com/adamchainz/django-jsonfield)).


## Django Settings

The following settings can be defined in your `SETTINGS.py`:

- **WAGTAILREFERENCES_CONVERT_BIBTEX** (default: `False`) Before saving new records, the record will be homogenized to
strict latex. This forces a conversion to unicode and, for example, adds braces to force capitalization.
- **WAGTAILREFERENCES_ENABLE_UNICODE** (default: `True`) If enabled, items such as `"C{\"o}ze"` will be converted to
their unicode equivalents. If you're using entries in a LaTeX rendering engine, this isn't necessary. If you're
using them to rendering HTML (which you probably are, this is a web CMS after all), you probably want this.
- **WAGTAILREFERENCES_COLLECTION_NAME** (default: `None`) Applies a default collection name to records rendered in bibjson form. 


## Examples

For your and our testing purposes, it's useful to have some examples to hand, so I've prepared some in the ``examples.py`` file, which simply contains a series of different bibtex references.

If you encounter awkward references or ones which won't validate, please post them into a github issue so I can help diagnose and add them for test.


## Thanks

Thanks are due to [**internaut**](https://github.com/internaut/bibtex2bibjson) for providing the bibtex-json converter. Their code isn't licensed so I don't know how to credit it other than saying thanks! 
