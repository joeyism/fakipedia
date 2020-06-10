import os
from flask import Flask, render_template, Markup, request, jsonify, render_template_string, redirect, url_for
from tqdm import tqdm
from models import text_generator
from lib import wikitext_to_html
from flask_sqlalchemy import SQLAlchemy
import logging
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
db = SQLAlchemy(app)
from lib import objects

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
  text_len = request.args.get("len", 250) or MAX_TEXT_LENGTH
  text_len = int(text_len)
  memory = request.args.get("memory", 1024) or DEFAULT_MODEL_MEMORY
  memory = int(memory)

  page = objects.GeneratedPage.get_page_by_query(title, text_len, memory)
  if page is None:
    cleaned_title = text_generator.clean_starting_text(title)
    cleaned_title = text_generator.create_starting_text(cleaned_title)
    source = text_generator.generate_text(cleaned_title, test=ENV.lower()=='test', text_len=text_len, memory=memory)
    source = wikitext_to_html.run(source)

    page = objects.GeneratedPage(title, cleaned_title, source, text_len, memory)
    page.save()

  source = """{% extends "layout.html" %}
  {% block title %}""" + page.title + """{% endblock %}

  {% block content %}
  """ + page.body + """
  {% endblock %}
  </div>
  """
  return render_template_string(source)

if __name__ == '__main__':
   app.run(debug=True)
