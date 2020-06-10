import os
from flask import Flask, render_template, Markup, request, jsonify, render_template_string, redirect, url_for, Response
from tqdm import tqdm
from flask_sqlalchemy import SQLAlchemy
import logging
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
db = SQLAlchemy(app)
from models import text_generator

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
  logging.info(request.args)
  search = request.args.get('search')
  text_len = request.args.get('len')
  memory = request.args.get('memory')
  
  search = search.replace(" ", "_")
  logging.info(f"Redirecting {search}")
  return render_template("redirect.html",
      model_url=url_for('generate_wiki', search=search, text_len=text_len, memory=memory),
      wiki_url=url_for('article', title=search, text_len=text_len, memory=memory)
  )

@app.route('/generate_wiki')
def generate_wiki():
  logging.info(request.args)
  search = request.args.get('search')
  text_len = request.args.get('len') or MAX_TEXT_LENGTH
  text_len = int(text_len)
  memory = request.args.get('memory') or DEFAULT_MODEL_MEMORY
  memory = int(memory)
  page = text_generator.generate_page(search, text_len, memory)
  return redirect(url_for('article', title=search, **request.args))

@app.route('/wiki/<title>')
def article(title):
  logging.info(f"Requesting article: {title}")
  text_len = request.args.get("len") or MAX_TEXT_LENGTH
  text_len = int(text_len)
  memory = request.args.get("memory") or DEFAULT_MODEL_MEMORY
  memory = int(memory)

  page = text_generator.generate_page(title, text_len, memory)

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
