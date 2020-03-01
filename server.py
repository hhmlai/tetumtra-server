from pyonmttok import Tokenizer
from ctranslate2 import Translator
from flask import Flask, jsonify, request
import logging
from logging.handlers import RotatingFileHandler

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
model = 'ct2_int16'
model_path = 'model/' + model
trans_ttpt = Translator(model_path = model_path + '/ttpt/')
trans_pttt = Translator(model_path = model_path + '/pttt/')
tokenizer_pttt = tokenizer_ttpt = Tokenizer("none", sp_model_path = 'model/ttpt.model')

@app.route('/', methods=['GET'])
def index():
    return 'Nada a ver aqui...'

@app.route('/trans/', methods=['POST'])
def translation():
    content = request.json
    app.logger.info(request.host + ': '+ str(content))
    pair = content['pair']
    text = content['text'][0]
    if pair == 'tt-pt':
                tokens, features = tokenizer_ttpt.tokenize(text)
                output = trans_ttpt.translate_batch(source=[tokens])
                response = tokenizer_ttpt.detokenize(output[0][0]['tokens']) 
    elif pair == 'pt-tt':
                tokens, features = tokenizer_pttt.tokenize(text)
                output = trans_pttt.translate_batch(source=[tokens])
                response = tokenizer_pttt.detokenize(output[0][0]['tokens']) 
    else:
                response = 'ERROR: unsuported pair'
    app.logger.info('translation: ' + response)
    return  jsonify({"translation":[response]})    

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s")
    handler = RotatingFileHandler('tetumtra.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.run(host='localhost', port=8081, debug=True)
# [END gae_python37_app]