import os
import logging
from flask import Flask, request, Response, jsonify
import socket
import cv2

# TODO remove if not needed
# grpcio>=0.15.0
# grpcio-tools>=0.15.0

from predict_client.prod_client import PredictClient

# Logger initialization
# This must happen before any calls to debug(), info(), etc.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# In each file/module, do this to get the module name in the logs
logger = logging.getLogger(__name__)

# API initialization
app = Flask(__name__)

MODEL_VERSION = 1

incv4_host = 'localhost:9000'

if 'INCV4_HOST' in os.environ:
    logger.info('Using ' + str(os.environ['INCV4_HOST']) + ' as host.')
    incv4_host = os.environ['INCV4_HOST']


hosts = {'incv4': PredictClient(incv4_host, 'incv4', 1)}


@app.route('/predict', methods=['POST'])
def predict():
    logger.info('/predict, hostname: ' + str(socket.gethostname()))

    if 'image' not in request.files:
        logger.info('Missing image parameter')
        return Response('Missing image parameter', 400)

    if 'model' not in request.form:
        logger.info('Missing image model parameter')
        return Response('Missing model parameter', 400)

    requested_model = request.form['model']

    if requested_model not in hosts:
        logger.info('Model ' + requested_model + ' not supported!')
        return Response('Model ' + requested_model + ' not supported!', 400)

    logger.info('Requested model: ' + requested_model)

    client = hosts[requested_model]

    # Write image to disk
    with open('request.jpg', 'wb') as f:
        f.write(request.files['image'].read())

    img = cv2.imread('request.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    prediction = client.predict(img)

    logger.info('Got prediction of length: ' + str(len(prediction)))

    ''' Convert the dict to json and return response '''
    return jsonify(
        prediction=prediction,
        prediction_length=len(prediction),
        hostname=str(socket.gethostname())
    )


@app.errorhandler(500)
def server_error(e):
    logger.error(str(e))
    response = Response('An internal error occurred. ' + str(e), 500)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
