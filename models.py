import app
from sqlalchemy.dialects.postgresql import JSON

class Image(app.db.Model):
	__tablename__ = 'images'

	id = app.db.Column(app.db.Integer, primary_key = True)
	url = app.db.Column(app.db.String())
	title = app.db.Column(app.db.String())
	caption = app.db.Column(app.db.String())
	location = app.db.Column(app.db.String())

	def __init__(self, url, title, caption, location):
		self.url = url
		self.title = title
		self.caption = caption
		self.location = location

	def __repr__(self):
		return '<id {}>'.format(self.id)
