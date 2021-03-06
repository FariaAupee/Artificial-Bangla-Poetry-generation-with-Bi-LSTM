# -*- coding: utf-8 -*-
"""file(KN).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sWkxqpd1fAKKv8_7TtC9BLpZAQmmRlpN
"""

from google.colab import drive
drive.mount('/content/drive')

import tensorflow as tf

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential, load_model, save_model,Model
from tensorflow.keras.optimizers import Adam
import numpy as np 
import re

tokenizer = Tokenizer(oov_token = "OOV")

whole_text = open("/content/drive/MyDrive/Bangla_Text_Generation/Dataset/Untitled folder/Nazrul.txt").read().lower()
whole_text  = whole_text.replace("\n", " ") 

whole_text  = whole_text.replace(",", " ,") 
whole_text  = whole_text.replace("।", " ।") 
whole_text  = whole_text.replace("?", " ?") 
whole_text  = whole_text.replace("!", " !") 
whole_text  = whole_text.replace("-", " - ") 


whole_text  = whole_text.replace("‘", "") 
whole_text  = whole_text.replace("’", "") 

whole_text  = re.sub(r'[" "]+', " ", whole_text)
whole_text  = whole_text.strip()

print(whole_text)

# cut the text in semi-redundant sequences of maxlen words
maxlen = 40
step = 10
corpus = []
wordlist = whole_text.split(" ")
for i in range(0, len(wordlist) - maxlen, step):
    corpus.append(" ".join(wordlist[i : i + maxlen]))

tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1

print(tokenizer.word_index)
print(total_words)

print(len(corpus))

print(corpus[0])

token_list = tokenizer.texts_to_sequences([corpus[0]])[0]
print(token_list)

token_list = tokenizer.texts_to_sequences([corpus[0]])[0]
for i in range(1, len(token_list)):
    n_gram_sequence = token_list[:i+1]
    print(n_gram_sequence)

input_sequences = []
for line in corpus:
  token_list = tokenizer.texts_to_sequences([line])[0]
  for i in range(1, len(token_list)):
    n_gram_sequence = token_list[:i+1]
    input_sequences.append(n_gram_sequence)

# pad sequences 
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

print(len(input_sequences))
# create predictors and label
xs, labels = input_sequences[:,:-1],input_sequences[:,-1]

ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

BUFFER_SIZE = 256
BATCH_SIZE = 64
steps_per_epoch = len(xs)//BATCH_SIZE

dataset = tf.data.Dataset.from_tensor_slices((xs, ys)).shuffle(BUFFER_SIZE)
dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)

model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
model.add(Bidirectional(LSTM(150)))
model.add(Dense(total_words, activation='softmax'))
adam = Adam(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
#earlystop = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto')
#print model.summary()
# print(model)

model.summary()

history = model.fit(dataset, epochs=100, verbose=1)

import matplotlib.pyplot as plt

def plot_graphs(history, string):
  plt.plot(history.history[string])
  plt.xlabel("Epochs")
  plt.ylabel(string)
  plt.show()

plot_graphs(history, 'accuracy')

plot_graphs(history, 'loss')

model.save("/content/drive/MyDrive/Bangla_Text_Generation/Model/modelNZ.h5")

import pickle
with open('/content/drive/MyDrive/Bangla_Text_Generation/Model/tokenizerNZ.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

from keras.models import load_model
# load model
model = load_model("/content/drive/MyDrive/Bangla_Text_Generation/Model/modelNZ.h5")

import pickle
# loading
with open('/content/drive/MyDrive/Bangla_Text_Generation/Model/tokenizerNZ.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

seed_text = "আমারে সকল ক্ষুদ্রতা হতে বাঁচাও প্রভু উদার। হে প্রভু​!"
next_words = 100
max_sequence_len = 40  
for _ in range(next_words):
	token_list = tokenizer.texts_to_sequences([seed_text])[0]
	token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
	predicted = model.predict_classes(token_list, verbose=0)
	output_word = ""
	for word, index in tokenizer.word_index.items():
		if index == predicted:
			output_word = word
			break
	seed_text += " " + output_word
print(seed_text)