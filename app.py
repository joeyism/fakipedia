from flask import Flask, render_template, Markup, request, jsonify, render_template_string
from tqdm import tqdm
from models import text_generator
from lib import wikitext_to_html

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
  return render_template(
      "index.html"
  )

@app.route('/wiki/<title>')
def article(title):
  source = text_generator.generate_text(title, test=True)
  source = wikitext_to_html.run(source)
  source = """{% extends "layout.html" %}
  <div id="content" class="mw-body" role="main">
  {% block content %}
  """ + source + """
  {% endblock %}
  </div>
  """
  return render_template_string(source)

if __name__ == '__main__':
   app.run(debug=True)
