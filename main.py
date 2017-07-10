# Python, flask and various api code imports
import os
import logging
from flask import Flask, request, Response, jsonify
import socket
import cv2

from predict_client import client

# Logger initialization
# This must happen before any calls to debug(), info(), etc.
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# In each file/module, do this to get the module name in the logs
logger = logging.getLogger(__name__)

# API initialization
app = Flask(__name__)

MODEL_NAME = 'mnist'
MODEL_VERSION = 1

MNIST_HOST = 'localhost'
MNIST_PORT = '9000'

if 'MNIST_HOST' in os.environ:
    MNIST_HOST = os.environ['MNIST_HOST']
    logger.info('Using: ' + MNIST_HOST)
else:
    logger.info('Using localhost')

if 'MNIST_PORT' in os.environ:
    MNIST_PORT = os.environ['MNIST_PORT']
    logger.info('Using: ' + MNIST_PORT)
else:
    logger.info('Using 9000')


@app.route('/predict', methods=['POST'])
def predict():
    logger.info('/predict, hostname: ' + str(socket.gethostname()))

    if 'image' not in request.files:
        logger.info('Missing image parameter')
        return Response('Missing image parameter', 400)

    # Write image to disk
    with open('request.png', 'wb') as f:
        f.write(request.files['image'].read())

    img = cv2.imread('request.png', 0)

    prediction = client.predict(img.reshape((img.shape + (1,))), MODEL_NAME, MODEL_VERSION,
                                host=MNIST_HOST, port=MNIST_PORT)

    logger.info('Prediction mnist image: ' + str(prediction))

    ''' Convert the dict to json and return response '''
    return jsonify(
        prediction=prediction,
        hostname=str(socket.gethostname())
    )


@app.errorhandler(500)
def server_error(e):
    logger.error(str(e))
    response = Response('An internal error occurred. ' + str(e), 500)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
