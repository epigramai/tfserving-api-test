import numpy as np
import tensorflow as tf
import grpc

# import predict_pb2
from predict_client.predict_pb2 import PredictRequest
# import prediction_service_pb2
from predict_client.prediction_service_pb2 import PredictionServiceStub


def predict(img,  model_name, model_version, host='localhost', port='9000'):
    REQUEST_TIMEOUT = 10
    host = host + ':' + port

    tensor_shape = (1,) + img.shape

    features_tensor_proto = tf.contrib.util.make_tensor_proto(img.reshape(tensor_shape),
                                                              dtype=tf.float32, shape=tensor_shape)

    # Create gRPC client and request
    channel = grpc.insecure_channel(host)
    stub = PredictionServiceStub(channel)
    request = PredictRequest()

    request.model_spec.name = model_name

    # request.model_spec.signature_name = 'serving_default'
    if model_version > 0:
        request.model_spec.version.value = model_version

    request.inputs['inputs'].CopyFrom(features_tensor_proto)

    # Send request
    result = stub.Predict(request, timeout=REQUEST_TIMEOUT)

    pred_label = np.argmax(result.outputs['scores'].float_val)

    return str(pred_label)


if __name__ == '__main__':
    import cv2
    img = cv2.imread('../data/correct-2-2.png', cv2.IMREAD_GRAYSCALE)
    # predict takes an image with shape (height, width, depth)
    img = img.reshape((img.shape + (1,)))
    pred = predict(img, 'mnist', 1)
    print(pred)
