import ctranslate2
import pyonmttok

def translate1(translator, batch_text, tokenizer):
  tokens, features = tokenizer.tokenize(batch_text[0])
  print(tokens)
  output = translator.translate_batch(source=[tokens])
  return tokenizer.detokenize(output[0][0]['tokens'])

tokenizer = Tokenizer("none", sp_model_path = 'model/ttpt.model')
trad_ttpt = ctranslate2.Translator(model_path = 'model/ct2_int16/pttt/')

def test(text):
    translation = translate1(trad_ttpt, text, tokenizer)
    print(translation)

test(["Teste aqui o tradutor."])