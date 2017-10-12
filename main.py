import os
import logging
from flask import Flask, request, Response, jsonify
import socket
import cv2
import numpy as np

from predict_client.prod_client import PredictClient

# Logger initialization
# This must happen before any calls to debug(), info(), etc.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# In each file/module, do this to get the module name in the logs
logger = logging.getLogger(__name__)

# API initialization
app = Flask(__name__)

MODEL_VERSION = 2

incv3_host = 'localhost:9000'
fashion_host = 'localhost:9001'

if 'INCV3_HOST' in os.environ:
    logger.info('Using ' + str(os.environ['INCV3_HOST']) + ' as incv3 host.')
    incv3_host = os.environ['INCV3_HOST']

if 'FASH_HOST' in os.environ:
    logger.info('Using ' + str(os.environ['FASH_HOST']) + ' as fash host.')
    fashion_host = os.environ['FASH_HOST']

clients = {'incv3': PredictClient(incv3_host, 'incv3', MODEL_VERSION),
           'fashion': PredictClient(fashion_host, 'fashion', 1)}


@app.route('/predict', methods=['POST'])
def predict():
    logger.info('/predict, hostname: ' + str(socket.gethostname()))

    if 'image' not in request.files:
        logger.info('Missing image parameter')
        return Response('Missing image parameter', 400)

    # Write image to disk
    with open('request.jpg', 'wb') as f:
        f.write(request.files['image'].read())

    img = cv2.imread('request.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (299, 299))

    img = img / 255
    img -= 0.5
    img *= 2

    prediction = clients['incv3'].predict(np.array([img]))
    print(len(prediction))

    fashion_pred = clients['fashion'].predict(np.array([prediction]))
    print(len(fashion_pred))

    fash_cat = np.argmax(fashion_pred)
    logger.info('Predicted: ' + str(fash_cat))

    ''' Convert the dict to json and return response '''
    return jsonify(
        prediction=str(fash_cat),
        hostname=str(socket.gethostname())
    )


@app.errorhandler(500)
def server_error(e):
    logger.error(str(e))
    response = Response('An internal error occurred. ' + str(e), 500)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
