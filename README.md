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
python manage migrate wagtail_references
```

## Reference Model

There's only one database model ``Reference``, which is registered as a snippet in Wagtail, making it searchable and
selectable.
