from app import db
from sqlalchemy.dialects.postgresql import JSON

class Image(db.Model):
	__tablename__ = 'images'

	id = db.Column(db.Integer, primary_key = True)
	url = db.Column(db.String())
	title = db.Column(db.String())
	caption = db.Column(db.String())
	location = db.Column(db.String())

	def __init__(self, url, title, caption, location):
		self.url = url
		self.title = title
		self.caption = caption
		self.location = location

	def __repr__(self):
		return '<id {}>'.format(self.id)
