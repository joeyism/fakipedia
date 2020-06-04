import os
from flask import Flask, render_template, Markup, request, jsonify, render_template_string
from tqdm import tqdm
from models import text_generator
from lib import wikitext_to_html
import logging

app = Flask(__name__)
ENV = os.getenv("ENV")
MAX_TEXT_LENGTH = os.getenv("MAX_TEXT_LENGTH", 250)

@app.route('/')
@app.route('/index')
def index():
  return render_template(
      "index.html"
  )

@app.route('/wiki/<title>')
def article(title):
  logging.info(f"Requesting article: {title}")
  input_str = text_generator.create_starting_text(title)
  source, cur_ids = text_generator.generate_text(input_str, test=ENV.lower()=='test', text_len=MAX_TEXT_LENGTH)
  source = wikitext_to_html.run(source)
  source = """{% extends "layout.html" %}
  {% block title %}""" + input_str + """{% endblock %}

  {% block content %}
  """ + source + """
  {% endblock %}
  </div>
  """
  return render_template_string(source)

if __name__ == '__main__':
   app.run(debug=True)
