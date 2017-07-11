# Python, flask and various api code imports
import logging
from flask import Flask, request, Response, jsonify
import socket
import cv2

from predict_client import client
from util.ports import get_port_mapping

# Logger initialization
# This must happen before any calls to debug(), info(), etc.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# In each file/module, do this to get the module name in the logs
logger = logging.getLogger(__name__)

# API initialization
app = Flask(__name__)

MODELS = ['mnist', 'res152', 'incv3', 'incv4']
MODEL_VERSION = 1
PORT_MAPPING = get_port_mapping(MODELS)


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

    if requested_model not in MODELS:
        logger.info('Model ' + requested_model + ' not supported!')
        return Response('Model ' + requested_model + ' not supported!', 400)

    logger.info('Requested model: ' + requested_model)

    host, port = PORT_MAPPING[requested_model]

    # Write image to disk
    with open('request.png', 'wb') as f:
        f.write(request.files['image'].read())

    if requested_model == 'mnist':
        img = cv2.imread('request.png', 0)
        logger.debug('Loaded request image shape: ' + str(img.shape))

        prediction = client.predict(img.reshape((img.shape + (1,))), requested_model, MODEL_VERSION,
                                    host=host, port=port)
    elif requested_model in ['incv3', 'incv4', 'res152']:
        img = cv2.imread('request.png')
        logger.debug('Loaded request image shape: ' + str(img.shape))

        prediction = client.predict(img, requested_model, MODEL_VERSION,
                                    host=host, port=port, is_batch_shaped=False)
    else:
        logger.warning('Check the if-else block above, this should not happen...')
        return Response('This should not happen...', 500)

    logger.info('Prediction of length:' + str(len(prediction)))

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
