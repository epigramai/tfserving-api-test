import os
import logging

logger = logging.getLogger(__name__)

MODEL_NAME = 'mnist'
MODEL_VERSION = 1

MNIST_HOST = 'localhost'
MNIST_PORT = '9000'


def get_port_mapping(model_names):

    port_mapping = {}

    for model in model_names:

        host = 'localhost'
        port = '9002'

        host_key = model.upper() + '_HOST'
        port_key = model.upper() + '_PORT'

        if host_key in os.environ:
            host = os.environ[host_key]

        logger.info('Using host ' + host + ' for model: ' + model)

        if port_key in os.environ:
            port = os.environ[port_key]

        logger.info('Using port ' + port + ' for model: ' + model)

        port_mapping[model] = (host, port)

    return port_mapping
