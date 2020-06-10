import os
from sqlalchemy import create_engine, MetaData
from lib import objects

engine = create_engine(os.getenv("DB_URL"))
if not engine.dialect.has_table(engine, objects.GeneratedPage):
  objects.GeneratedPage.__table__.create(bind=engine, checkfirst=True)
