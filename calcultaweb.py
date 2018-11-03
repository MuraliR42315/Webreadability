import textstat
import string
import re
from pyphen import Pyphen
import pandas as pd 
import urllib
from bs4 import BeautifulSoup
from sklearn.tree import DecisionTreeClassifier
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import train_test_split
exclude =list(string.punctuation)
def gettext(url):
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html)
	for script in soup(["script", "style"]):
    		script.extract()  
	text = soup.get_text()
	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text

def syllable_count(text, lang='en_US'):
	text=text.lower()
	text="".join(x for x in text if x not in exclude)
	if text is None:
		return 0
	elif len(text)==0:
		return 0
	else:
		dic =Pyphen(lang=lang)
		count =0
		for word in text.split(' '):
			word_hyphenated = dic.inserted(word)
			count+=max(1,word_hyphenated.count("-")+1)
		return count

def lexicon_count(text, removepunct =True):
	if removepunct:
		text=''.join(ch for ch in text if ch not in exclude)
 	count = len(text.split())
	return count
	

def sentence_count(text):
	ignoreCount=0
	sentences=re.split(r' *[\.\?!][\'"\)\]]* *',text)
	for sentence in sentences:
		if lexicon_count(sentence)<=2:
			ignoreCount = ignoreCount+1
	return max(1,len(sentences)- ignoreCount)

def avg_sent_len(text):
	lc=lexicon_count(text)
	sc=sentence_count(text)
	if sc==0: 
		return 0.1
	else:
		ASL=float(lc/sc)
		return ASL	

def avg_syll_word(text):
	syllable=syllable_count(text)
	words=lexicon_count(text)
	if words==0:
		return 1
	else:
		ASPW=float(syllable)/float(words)
		return ASPW

def calculate(text):
	ASL=avg_sent_len(text)
	ASW=avg_syll_word(text)	
	FRE=206.835-float(1.015*ASL)-float(84.6*ASW)
	return FRE

def polysyllabcount(text):
        count = 0
        for word in text.split():
            wrds = syllable_count(word)
            if wrds >= 3:
                count += 1
	return count	


def rareword(text):
	c=1
	words = word_tokenize(text)
	rare="gypbvkjxqz"
	for w in words:
		for i in w:
			if i in rare:
				c=c+1
				break		
	return c	

def ttrc(text):
	tokens = word_tokenize(text)
	types=[]
	for t in tokens:
		if t not in types:
			types.append(t)
	#print type(len(tokens))
	#print type(len(types))
	#print len(tokens)
	#print len(types)
	if len(tokens)==0:
		return 0.1
	else:
		return float(len(types))/float(len(tokens))		
	

from nltk.corpus import wordnet as wn
def lexmbcount(text):
	c=0
	words = word_tokenize(text)
	for w in words:
		synsets = wn.synsets(w)
		if len(synsets)>2:
			c=c+1		
	return c

def cal(url):
	data1=[]
	text=gettext(url)
	val= calculate(text)
	lc=lexicon_count(text)
	sc=sentence_count(text)
	asl=avg_sent_len(text)
	sylc=syllable_count(text)
	asyw=avg_syll_word(text)
	polsc=polysyllabcount(text)
	rarewc=rareword(text)
	ttr=ttrc(text)
	lexamc=lexmbcount(text)
	if val< 45:
		d=0
	elif val< 64:
		d=1
	else:
		d=2
	if val>90:
		e=0
	elif val>80:
		e=1
	elif val>64:
		e=2
	elif val>56:
		e=3
	elif val>45:
		e=4
	elif val>30:
		e=5
	else:
		e=6
	list=[[lc, sc, asl, sylc, asyw, polsc, rarewc,ttr, lexamc,d,e]]
	X=pd.DataFrame(list)
	X.to_csv("read.csv")
	fp1=pd.read_csv("read.csv")
	data1=fp1.values
	X_test=data1[:,0:8]
	Y_test=data1[:,-2]
	fp = pd.read_csv("rating.csv")
	data = fp.values
	X_train= data[:,0:8]
	Y_train = data[:, -2]
	seed = 	50
	#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=seed)
	clf= dtc= DecisionTreeClassifier()
	clf.fit(X_train, Y_train)
	y_pred = clf.predict(X_test)
	print "y_pred="+str(y_pred)
	print "y_test="+str(Y_test)
	if y_pred==0:
		print "Less Readable"
	elif y_pred==1:
		print "Readable"
	else:
		print "Highly Readable"
	X_test=data1[:,0:8]
	Y_test=data1[:,-1]
	fp = pd.read_csv("rating.csv")
	data = fp.values
	X_train= data[:,0:8]
	Y_train = data[:,-1]
	seed = 	50
	#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=seed)
	clf= dtc= DecisionTreeClassifier()
	clf.fit(X_train, Y_train)
	y_pre = clf.predict(X_test)
	print "y_pred="+str(y_pre)
	print "y_test="+str(Y_test)
	if y_pre==0:
		print "5th grade"
	elif y_pre==1:
		print "6th grade"
	elif y_pre==2:
		print "7th grade"
	elif y_pre==3:
		print "8 & 9th grade"
	elif y_pre==4:
		print "10 & 12th grade"
	elif y_pre==5:
		print "college grade"
	else:
		print "graduate"
	return y_pred,y_pre
	
	



