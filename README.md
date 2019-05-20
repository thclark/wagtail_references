# Wagtail References [![Build Status](https://travis-ci.com/thclark/wagtail_references.svg?branch=master)](https://travis-ci.com/thclark/wagtail_references)

BibTeX based bibliography entries, as wagtail snippets


## Templates

**"But, where are the templates?!"** is a natural question. Answer: There aren't any templates or tags so far...
I run all my wagtail installations in headless mode with a react front end, so can only justify putting in place the
templates for managing the references on wagtail (for now). But see below for how to do it yourself.

If you'd like to make a PR with tmplates, I'm very open to collaboration :)

I'm gradually improving wagtail admin templates, I'll do an ever-better job as the library gets more traction and users.
**Bottom line: Star this repo on Github if you use or like it, so I know it's getting traction!** 


## Displaying references on the front end

### Write your own templates/html

I use [citation.js](https://citation.js.org/api/tutorial-getting_started.html) for parsing and displaying the bibtex 
in the wagtail admin, it's usable in-browser (in a template) like this:

```html
<!-- Using citation.js https://citation.js.org/api/tutorial-getting_started.html -->
<script src="https://cdn.jsdelivr.net/npm/citation-js" type="text/javascript"></script>
<script type="text/javascript">
  const Cite = require('citation-js')
  function renderToDiv(inputBibtex, divId) {
      const citation = new Cite(inputBibtex)
      const outputHtml = citation.format('bibliography', {
        format: 'html',
        template: 'apa',
        lang: 'en-US'
      })
      outputDiv = document.getElementById(divId)
      outputDiv.innerHTML = outputHtml
  }
</script>

<h3><strong>Slug (citation key):</strong> {{ reference.slug }}</h3>
<h3><strong>Type:</strong> {{ reference.bibtype }}</h3>
<div id="{{ reference.slug }}"></div>
<script type="text/javascript"> renderToDiv("{{ reference.bibtex_string }}", "{{ reference.slug }}") </script>
```

### Using react (wagtail in headless mode)

On the frontend, I use react (see aforementioned nanorant about using wagtail in a headless mode). I'm presently using 
[react-citeproc](https://github.com/robindemourat/react-citeproc) along with
 [biblatex-csl-converter](https://github.com/fiduswriter/biblatex-csl-converter) in a project and it works out pretty
 well. Your component will look like this-ish:
 
```javascript
import React from 'react'
import { Bibliography } from 'react-citeproc'
import raw from 'raw.macro'

import { BibLatexParser, CSLExporter } from 'biblatex-csl-converter'

const style = raw('assets/csl/apa-style.csl')
const locale = raw('assets/csl/xml-locale.xml')

class Reference extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      bibtex: undefined,
      csl: undefined,
    }
  }

  static getDerivedStateFromProps(nextProps, prevState) {
    if (nextProps.bibtex !== prevState.bibtex) {
      const parser = new BibLatexParser(nextProps.detail.bibtex, { processUnexpected: false, processUnknown: false })
      const csl = new CSLExporter(parser.output).parse()
      return {
        bibtex: nextProps.detail.bibtex,
        csl,
      }
    }
    return null
  }

  render() {
    return (
      <div className={classes.bibliography}>
        <Bibliography
          style={style}
          locale={locale}
          items={this.state.csl}
        />
      </div>
    )
  }
}

export default Reference
```



## Roadmap

I'd like to include:
- A better snippet editor, possibly using a json editor component and allowing the user to switch between tex and json
- A `ListSerializer` for serializing out multiple references as a bibjson collection
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
