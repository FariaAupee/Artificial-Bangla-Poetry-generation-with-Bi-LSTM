from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import time
import helper

app = Flask(__name__)

def predict():
    with popup("Artificial Bangla Poetry Generation"):
        put_text("Welcome")

    put_text("input sequence:-")
    seed_text = input()
    put_text(seed_text)
    put_text("number of next predicted words:-")
    n_words = input()
    put_text(n_words)
    put_text("specify writing pattern: R/N?")
    auth = input()

    if auth == "R" :
         put_text("Rabindranath is selected.")
         Model = helper.load_modelRT()
         dictionary = helper.load_dictionaryRT()
         put_processbar('bar')
         for i in range(1,11):
            set_processbar('bar',i/10)
            time.sleep(0.2)
    
    elif auth == "N":
        put_text("Nazrul is selected.")
        Model = helper.load_modelNZ()
        dictionary = helper.load_dictionaryNZ()
        put_processbar('bar')
        for i in range(1,11):
            set_processbar('bar',i/10)
            time.sleep(0.2)

    else:
        #put_text
        put_error("Invalid selection")
        return

    pred = helper.generate_words(Model,dictionary,40,seed_text,int(n_words))
    put_text("Generated text: " ,pred)

    app.add_url_rule('/tool','webio_view', webio_view(predict),
                     methods = ['GET','POST','OPTIONS'])
    app.run(host= 'localhost', port=80,)

if __name__ == "__main__":
    predict()