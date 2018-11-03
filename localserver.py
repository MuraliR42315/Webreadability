from flask import Flask, request,jsonify,Response,render_template,url_for
import subprocess
import os, platform
import textstat
import string
import calcultaweb
import numpy as np
import json
import re
from pyphen import Pyphen
import pandas as pd 
import urllib
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import train_test_split
exclude =list(string.punctuation)



app = Flask(__name__)
@app.route('/download' , methods=['POST'])
def start_download():
	if request.method == 'POST':
		url=request.form['url']
		status=request.form['status']
		read,grade=calcultaweb.cal(url)
		read=str(read[0])
		grade=str(grade[0])
		if(status=='check'):
			print(read,grade)
			output=[read,grade]
			output=json.dumps(output)
			return output,200
	else:
		print("Bad Request")

@app.route('/')
def hello():
    return 'Local server ON'

if __name__ == '__main__':
    app.run(debug=True,threaded=True)
