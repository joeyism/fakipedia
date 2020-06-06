import os
from flask import Flask, render_template, Markup, request, jsonify, render_template_string, redirect, url_for
from tqdm import tqdm
from models import text_generator
from lib import wikitext_to_html
import logging

app = Flask(__name__)
ENV = os.getenv("ENV")
MAX_TEXT_LENGTH = os.getenv("MAX_TEXT_LENGTH", 250)
DEFAULT_MODEL_MEMORY = os.getenv("DEFAULT_MODEL_MEMORY", 1024)

@app.route('/')
@app.route('/index')
def index():
  return render_template(
      "index.html"
  )

@app.route('/redirect')
def redirect_search():
  search = request.args.get('search')
  search = search.replace(" ", "_")
  logging.info(f"Redirecting {search}")
  return redirect(url_for('article', title=search))

@app.route('/wiki/<title>')
def article(title):
  logging.info(f"Requesting article: {title}")
  text_len = request.args.get("len") or MAX_TEXT_LENGTH
  text_len = int(text_len)
  memory = request.args.get("memory") or DEFAULT_MODEL_MEMORY

  cleaned_title = text_generator.clean_starting_text(title)
  input_str = text_generator.create_starting_text(cleaned_title)
  source = text_generator.generate_text(input_str, test=ENV.lower()=='test', text_len=text_len)
  source = wikitext_to_html.run(source)
  source = """{% extends "layout.html" %}
  {% block title %}""" + cleaned_title + """{% endblock %}

  {% block content %}
  """ + source + """
  {% endblock %}
  </div>
  """
  return render_template_string(source)

if __name__ == '__main__':
   app.run(debug=True)
