from mediawiki_parser import preprocessor, raw, text, html
import py3compat

allowed_tags = ['p', 'span', 'b', 'i']
allowed_autoclose_tags = ['br', 'hr']
allowed_parameters = ['class', 'style', 'name', 'id', 'scope']
interwiki = {'en': 'http://en.wikipedia.org/wiki/',
             'fr': 'http://fr.wikipedia.org/wiki/'}
namespaces = {'Template':   10,
              u'Catégorie': 14,
              'Category':   14,
              'File':        6,
              'Image':       6}
parser = html.make_parser(allowed_tags, allowed_autoclose_tags, allowed_parameters, interwiki, namespaces)
preprocessor_parser = preprocessor.make_parser({})

def parse(source):
  source = source.strip()
  if not source.endswith("\n"):
    source += "\n"
  preprocessed = preprocessor_parser.parseTest(source).value
  return py3compat.text_type(parser.parseTest(preprocessed).leaves())
