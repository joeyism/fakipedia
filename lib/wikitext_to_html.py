from mediawiki_parser import preprocessor, raw, text, html
import py3compat
import lxml.html

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
siteSubElem = lxml.html.fromstring('<div class="siteSub">From Fakipedia, the fake Wikipedia</div><div class="contentSub"/>')

def preprocess(source):
  source = source.replace("\n ", "\n") \
                .replace(" \n", "\n") \
                .replace("= ", "=") \
                .replace(" =", "=") \
                .replace("@ ", " ") \
                .replace(" @", " ") \
                .strip()
  source_split = source.split("\n")
  # fixing title
  source_split[0] = source_split[0].replace("==", "=")

  for i, sentence in enumerate(source_split):
    if "=" not in sentence:
      continue
    name = "".join(sentence.split("="))
    begin = sentence.split(name)[0]
    sentence = begin + name + begin
    source_split[i] = sentence

  source = "\n".join(source_split)
  return source

def process(source):
  source = source.strip()
  if not source.endswith("\n"):
    source += "\n"
  preprocessed = preprocessor_parser.parseTest(source).value
  return py3compat.text_type(parser.parseTest(preprocessed).leaves())

def postprocess(source):
  main_elem = lxml.html.fromstring(source)
  header = main_elem.find(".//h1")
  if header is not None:
    main_elem.insert(main_elem.index(header) + 1, siteSubElem)
  return lxml.html.tostring(main_elem).decode("utf8")

def run(source):
  source = preprocess(source)
  source = process(source)
  source = postprocess(source)
  return source
