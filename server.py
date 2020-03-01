from pyonmttok import Tokenizer
from ctranslate2 import Translator
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Nada a ver aqui...'

@app.route('/trans/', methods=['POST'])
def translation():
    content = request.json
    model = content['model']
    print(model)
    text = content['text'][0]
    translator = Translator(model_path = 'model/' +  model)
    tokenizer = Tokenizer("none", sp_model_path = 'model/ttpt.model')
    tokens, features = tokenizer.tokenize(text)
    output = translator.translate_batch(source=[tokens])
    response = tokenizer.detokenize(output[0][0]['tokens']) 
    return  jsonify({"translation":[response]})    

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='localhost', port=8081, debug=True)
