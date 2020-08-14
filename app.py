#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models

images = []

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/image_sharing/api/v1.0/images', methods=['GET'])
def get_images():
	# return jsonify({'images': images})
	displayed_images = []
	# try:
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
	# except:
	# 	abort(500)

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
	# image = [image for image in images if image['id'] == image_id]
	# if len(image) == 0:
	# 	abort(404)
	# return jsonify({'image': image[0]})

@app.route('/image_sharing/api/v1.0/images', methods=['POST'])
def create_image():
	if not request.json or not 'url' in request.json:
		abort(400)
	# image = {
	# 	'id': images[-1]['id'] + 1,
	# 	'url': request.json['url'],
	# 	'title': request.json['title'],
	# 	'caption': request.json.get('caption', ""),
	# 	'location': request.json['location']
	# }
	try:
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
	except:
		abort(500)
	# images.append(image)

@app.route('/image_sharing/api/v1.0/images/<int:image_id>', methods=['PUT'])
def update_image(image_id):
	image = [image for image in images if image['id'] == image_id]
	if len(image) == 0:
		abort(404)
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
	image[0]['url'] = request.json.get('url', image[0]['url'])
	image[0]['title'] = request.json.get('title', image[0]['title'])
	image[0]['caption'] = request.json.get('caption', image[0]['caption'])
	image[0]['location'] = request.json.get('location', image[0]['location'])
	return jsonify({'image': image[0]})

@app.route('/image_sharing/api/v1.0/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
	image = [image for image in images if image['id'] == image_id]
	if len(image) == 0:
		abort(404)
	images.remove(image[0])
	return jsonify({'result': True})

if __name__ == '__main__':
	app.run(debug=True)
