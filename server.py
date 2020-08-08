from pyonmttok import Tokenizer
from ctranslate2 import Translator
from flask import Flask, jsonify, request
from google.cloud import datastore
from datetime import datetime

client = datastore.Client()

app = Flask(__name__)

max_size = 500
@app.route('/', methods=['GET'])
def index():
    return 'Nada a ver aqui...'

@app.route('/trans/', methods=['POST'])
def translation():
    content = request.json
    model = content['model']
    pair = content['pair']
    model_path = 'models/' + model + '/' + pair + '/'
    text_list = content['text'].splitlines()
    res_list = []
    for text in text_list:
        text = text[:max_size].strip()
        if len(text) > 0:
            translator = Translator(model_path = model_path)
            tokenizer = Tokenizer("none", sp_model_path = model_path + 'vocab.model')
            tokens, features = tokenizer.tokenize(text)
            output = translator.translate_batch(source=[tokens])
            response = tokenizer.detokenize(output[0][0]['tokens'])
            res_list.append(response) 
    translation = '\n'.join(res_list)
    time = datetime.utcnow().isoformat()
    key = client.key('translation', time)
    task = datastore.Entity(key)
    task.update({
        'pair': pair,
        'model': model,
        'text': content['text'],
        'translation': translation,
        'time': time,
        'ip': request.remote_addr
    })
    client.put(task)
    return  jsonify({"translation": translation})    

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='localhost', port=8081, debug=True)
