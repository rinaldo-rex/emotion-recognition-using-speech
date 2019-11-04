"""
A simple wrapper for emotion recognition that you can directly use to check this out.
"""

from flask import request, Flask, jsonify, render_template
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.propagate = False

from emotion_recognition import EmotionRecognizer
from sklearn.svm import SVC
from deep_emotion_recognition import DeepEmotionRecognizer



# init a model, let's use SVC
my_model = SVC()
# pass my model to EmotionRecognizer instance
# and balance the dataset
simple_emotion = EmotionRecognizer(model=my_model, emotions=['sad', 'neutral',
                                                             'happy', 'fear'],
                                   balance=True, verbose=0)
# train the model
simple_emotion.train()

# initialize instance
# inherited from emotion_recognition.EmotionRecognizer
# default parameters (LSTM: 128x2, Dense:128x2)
deep_emotion = DeepEmotionRecognizer(emotions=['angry', 'sad', 'neutral', 'ps', 'happy'], n_rnn_layers=2, n_dense_layers=2,
                          rnn_units=128, dense_units=128)
# train the model
deep_emotion.train()



app = Flask(__name__)


def get_simple_emotion(wav_path):

    emotion = simple_emotion.predict(wav_path)
    return str(emotion)


def get_deep_emotion(wav_path):
    emotion = deep_emotion.predict(wav_path)

    return str(emotion)


@app.route('/simple-emotion')
def fetch_simple_emotion():
    if not os.path.exists('Audio'):
        os.mkdir('Audio')
    f = request.files['file']

    # FIXME: USE PATHLIB! 🤷🏻‍♂️
    f.save('Audio/' + f.filename)

    s_emotion = get_simple_emotion('Audio/' + f.filename)
    # FIXME: Deepemotion has tensor shape problem as of now.
    # deep_emotion = get_deep_emotion('Audio/fear.wav')

    return jsonify({
        "data": {
            "emotion": {
                "simple": s_emotion,
                # "deep": deep_emotion,
            },
        }
    })


if __name__ == '__main__':
    app.run(debug=True, port=5678)
