from app import db

class GeneratedPage(db.Model):
  __tablename__ = 'generated_pages'

  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(256), nullable=False)
  title = db.Column(db.String(256), nullable=False)
  body = db.Column(db.Text, nullable=False)
  length = db.Column(db.Integer, nullable=False)
  memory = db.Column(db.Integer, nullable=False)

  def __init__(self, url, title, body, length, memory):
    self.url = url
    self.title = title
    self.body = body
    self.length = length
    self.memory = memory

  def save(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_page_by_url(cls, url):
    return db.session.query(User).filter_by(url=url).first()

  @classmethod
  def get_page_by_query(cls, url, length, memory):
    return db.session.query(GeneratedPage).filter_by(url=url, length=length, memory=memory).first()
