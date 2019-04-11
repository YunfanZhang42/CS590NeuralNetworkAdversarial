import base64
import os
import json
import uuid

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from NeuralNet.fool import fool, load_image

STATIC_FOLDER = '/Users/yunfan/PycharmProjects/CS590NeuralNetworkAdversarial/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_url_path='/static')
app.config['STATIC_FOLDER'] = STATIC_FOLDER
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').strip('=') + '_' + filename
        file.save(os.path.join(app.config['STATIC_FOLDER'], filename))
        return json.dumps({'url': 'static/' + filename}), 201


@app.route('/run', methods=['POST'])
def run():
    original_url = request.json['originalURL']
    transform_category = request.json['category']
    result = fool(load_image(original_url), transform_category)
    noise_url = 'static/' + base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').strip('=') + '.png'
    noise10x_url = 'static/' + base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').strip('=') + '.png'
    transformed_url = 'static/' + base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').strip('=') + '.png'

    result['diff'].save(noise_url)
    result['diff10'].save(noise10x_url)
    result['fooled_img'].save(transformed_url)

    response = {
        'originalResult': result['original_res'],
        'originalConfidence': int(result['original_conf'] * 100),
        'transformedResult': result['fooled_res'],
        'transformedConfidence': int(result['fooled_conf'] * 100),
        'noiseURL': noise_url,
        'noise10xURL': noise10x_url,
        'transformedURL': transformed_url
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run()
