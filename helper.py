import pickle
import os
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential,load_model,save_model,Model
from tensorflow.keras.optimizers import Adam

def load_modelRT():
        model = load_model("./modelRT.h5")
        return model

def load_dictionaryRT():
     with open("./tokenizerRT.pickle", 'rb') as f:
        dict = pickle.load(f)
        return dict

def load_modelNZ():
        model = load_model("./modelNZ.h5")
        return model

def load_dictionaryNZ():
     with open("./tokenizerNZ.pickle", 'rb') as f:
        dict = pickle.load(f)
        return dict

def generate_words(__model, __dict, text_seq_length, seed_text, n_words):
    #text = []
    #print("generate_words")
    for _ in range(n_words):
        #print(n_words)
        token_list = __dict.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=text_seq_length - 1, padding='pre')
        print(token_list)
        predicted = __model.predict_classes(token_list)
        #print(predicted)
        output_word = ""
        for word, index in __dict.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
        #text.append(output_word)
        #return ' '.join(text)
    return seed_text