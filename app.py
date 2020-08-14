#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

images = []

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/image_sharing/api/v1.0/images', methods=['GET'])
def get_images():
	return jsonify({'images': images})

@app.route('/image_sharing/api/v1.0/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
	image = [image for image in images if image['id'] == image_id]
	if len(image) == 0:
		abort(404)
	return jsonify({'image': image[0]})

@app.route('/image_sharing/api/v1.0/images', methods=['POST'])
def create_image():
	if not request.json or not 'url' in request.json:
		abort(400)
	image = {
		'id': images[-1]['id'] + 1,
		'url': request.json['url'],
		'title': request.json['title'],
		'caption': request.json.get('caption', ""),
		'location': request.json['location']
	}
	images.append(image)
	return jsonify({'image': image}), 201

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
