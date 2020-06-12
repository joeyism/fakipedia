import os
from flask import Flask, render_template, Markup, request, jsonify, render_template_string, redirect, url_for, Response
from tqdm import tqdm
from flask_sqlalchemy import SQLAlchemy
import logging
from models import text_generator
from lib import objects

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
db = SQLAlchemy(app)


MAX_TEXT_LENGTH = os.getenv("MAX_TEXT_LENGTH", 1024)
DEFAULT_MODEL_MEMORY = os.getenv("DEFAULT_MODEL_MEMORY", 200)

@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html",
      DEFAULT_TEXT_LENGTH=MAX_TEXT_LENGTH,
      DEFAULT_MODEL_MEMORY=DEFAULT_MODEL_MEMORY
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
      model_url=url_for('generate_wiki', search=search, len=text_len, memory=memory),
      wiki_url=url_for('article', title=search, len=text_len, memory=memory)
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

@app.route('/about_us')
def about_us():
  return render_template("about_us.html")

@app.route('/random')
def random():
  page = objects.GeneratedPage.get_random_page()
  return redirect(url_for('article', title=page.url, len=page.length, memory=page.memory))

if __name__ == '__main__':
   app.run(debug=True)
