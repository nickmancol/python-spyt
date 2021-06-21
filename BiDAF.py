import numpy as np
import string
import onnx
import os
import glob
import nltk
import onnxruntime as rt
from nltk import word_tokenize
from onnx import numpy_helper

sess = rt.InferenceSession("model/bidaf-9.onnx")
nltk.download('punkt')

def preprocess(text):
   tokens = word_tokenize(text)
   # split into lower-case word tokens, in numpy array with shape of (seq, 1)
   words = np.asarray([w.lower() for w in tokens]).reshape(-1, 1)
   # split words into chars, in numpy array with shape of (seq, 1, 1, 16)
   chars = [[c for c in t][:16] for t in tokens]
   chars = [cs+['']*(16-len(cs)) for cs in chars]
   chars = np.asarray(chars).reshape(-1, 1, 1, 16)
   return words, chars

# input
context = ''''''
query = 'what is the Iron Man 2?'
cw, cc = preprocess(context)
qw, qc = preprocess(query)

inputs = [cw, cc, qw, qc]

print("Model inputs")
for input in sess.get_inputs():
    print(input.name)

inputs = {}
inputs['context_word'] = cw
inputs['context_char'] = cc
inputs['query_word'] = qw
inputs['query_char'] = qc

print("Model outputs")
outputs = []
for output in sess.get_outputs():
    print(output.name)
    outputs.append(output.name)

answer = list( sess.run( outputs, inputs ) )
start = np.asscalar(answer[0])
end = np.asscalar(answer[1])
print(' '.join([bytes.decode(w.encode()) for w in cw[start:end+1].reshape(-1)]))
