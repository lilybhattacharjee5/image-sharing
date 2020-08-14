#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/image_sharing/api/v1.0/images', methods=['GET'])
def get_images():
	displayed_images = []
	try:
		images = db.session.query(models.Image).all()
		for image in images:
			displayed_images.append({
				id: image.id,
				url: image.url,
				title: image.title,
				caption: image.caption,
				location: image.location
			})
		return jsonify({'images': displayed_images})
	except:
		abort(500)

@app.route('/image_sharing/api/v1.0/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
	try:
		image = db.session.query(models.Image).get(image_id)
		displayed_image = {
			id: image.id,
			url: image.url,
			title: image.title,
			caption: image.caption,
			location: image.location
		}
		return jsonify({'image': displayed_image})
	except:
		abort(500)

@app.route('/image_sharing/api/v1.0/images', methods=['POST'])
def create_image():
	if not request.json or not 'url' in request.json:
		abort(400)
	# try:
	image = models.Image(
		url = request.json['url'],
		title = request.json['title'],
		caption = request.json['caption'],
		location = request.json['location']
	)
	db.session.add(image)
	db.session.commit()

	displayed_image = {
		'id': image.id,
		'url': image.url,
		'title': image.title,
		'caption': image.caption,
		'location': image.location
	}
	return jsonify({'image': displayed_image}), 201
	# except:
	# 	abort(500)

@app.route('/image_sharing/api/v1.0/images/<int:image_id>', methods=['PUT'])
def update_image(image_id):
	if not request.json:
		abort(400)
	if 'url' in request.json and type(request.json['url']) != unicode:
		abort(400)
	if 'title' in request.json and type(request.json['title']) != unicode:
		abort(400)
	if 'caption' in request.json and type(request.json['caption']) != unicode:
		abort(400)
	if 'location' in request.json and type(request.json['location']) != unicode:
		abort(400)
	try:
		image = db.session.query(models.Image).get(image_id)
		image.update({
			'url': image.url if 'url' not in request.json else request.json['url'],
			'title': image.title if 'title' not in request.json else request.json['title'],
			'caption': image.caption if 'caption' not in request.json else request.json['caption'],
			'location': image.location if 'location' not in request.json else request.json['location']
		})
		db.session.commit()
		displayed_image = {
			id: image.id,
			url: image.url,
			title: image.title,
			caption: image.caption,
			location: image.location
		}
		return jsonify({'image': displayed_image})
	except:
		abort(500)

@app.route('/image_sharing/api/v1.0/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
	try:
		db.session.query(models.Image).filter_by(id=image_id).delete()
		db.session.commit()
	except:
		abort(500)
	return jsonify({'result': True})

if __name__ == '__main__':
	app.run(debug=True)
