# Packages for data processing 
import numpy as np, pandas as pd, math, random
#Packages for webpage crawling
import requests as r
import re
from bs4 import BeautifulSoup as BS
#Packages for nature language processing
import spacy,pyinflect
from pyinflect import getAllInflections
import nltk,string,re,emoji
from collections import Counter
from nltk.corpus import stopwords as sw
from nltk.util import ngrams as ng
from nltk.tokenize import word_tokenize as tk
from nltk.stem import WordNetLemmatizer as wn
import gender_guesser.detector as gen
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import sentiwordnet as swn
#Packages for machine learning (flair and bert_based model)
from flair.models import TARSClassifier
from flair.data import Sentence
import tweetnlp
import gensim
#Packages for LDA Visualisation
import pyLDAvis
import pyLDAvis.gensim_models
#Packages for Twitter API and configuration
import tweepy as tw, configparser  
#Packages about time
import time as t, datetime as dt, rfc3339
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
#Packages for visualisation
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')


nlp = spacy.load('en_core_web_md')
#Remove all the emoji used in the text
def emoji_free_text(text):
    pattern = re.compile(pattern = 
    '[' u'\U0001F600-\U0001F64F'  # emoticons
        u'\U0001F300-\U0001F5FF'  # symbols & pictographs
        u'\U0001F680-\U0001F6FC'  # transport & map symbols
        u'\U0001F1E6-\U0001F1FF'  # flags (iOS)
        u'\U00002500-\U00002BEF'  # chinese char
        u'\U00002702-\U000027B0'
        u'\U000024C2-\U0001F251'
        u'\U0001f926-\U0001f937'
        u'\U00010000-\U0010ffff'
        u'\u2640-\u2642'
        u'\u2600-\u2B55'
        u'\u23cf'
        u'\u23e9'
        u'\u231a'
        u'\u3030'
        u'\ufe0f'
        u'\u200a-\u200f'']+', 
        flags = re.UNICODE)
    return pattern.sub(r'',text)

# text modification
def delete_repetition(emoji_content, max_times=2):
    emoji=list(emoji_content)
    emotion=' '.join(emoji_content)
    checklist = [lab for lab in dict.fromkeys(emoji) if emoji.count(lab) > 1]
    for i in range(len(checklist)):
        while(emoji.count(checklist[i]) > max_times):
            emoji.remove(checklist[i])
            emotion=''.join(emoji)
    return emotion

def remove_duplicate_emoji(text):
    pure_text=emoji_free_text(text)
    duplicate_emoji = []
    for emo in text:
        if emo in (emoji.UNICODE_EMOJI['en'] or emoji.UNICODE_EMOJI['es'] or emoji.UNICODE_EMOJI['pt'] or emoji.UNICODE_EMOJI['it']):
            duplicate_emoji.append(emo)
    twice_maximum=delete_repetition(duplicate_emoji)
    text=pure_text+twice_maximum
    return text

def free_contact(text):
    text=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
    return text

#Restore all emoji into readable meanings
def emoji_lemon(text):
    return emoji.demojize(text, delimiters=('', ' ')) 

def single_quote_transfer(text):
    text=re.sub('  ',' ',text)
    text=re.sub("'ve",' have',text)
    text=re.sub("'d",' would like to',text)
    text=re.sub("n't",' not',text)
    text=re.sub("'m",' am',text)
    text=re.sub("'s",' is',text)
    text=re.sub('_',' ',text)
    text=re.sub('hrs','hours', text)
    text=re.sub('pls','please', text)
    text=re.sub('bf','boyfriend',text)
    text=re.sub('dcpc','driver certificate of professional competence', text)
    text=re.sub('celebs','celebrities', text)
    cos='cos'
    bcos='bcos'
    rd='rd'
    mon='mon'
    tue='tues'
    wed='wed'
    thu='thu'
    fri='fri'
    sat='sat'
    tfl='tfl'
    amp='amp'
    text=re.compile(r'\b%s\b' % cos, re.I).sub('because',text)
    text=re.compile(r'\b%s\b' % bcos, re.I).sub('because',text)
    text=re.compile(r'\b%s\b' % rd, re.I).sub('road',text)
    text=re.compile(r'\b%s\b' % mon, re.I).sub('monday',text)
    text=re.compile(r'\b%s\b' % tue, re.I).sub('tuesday',text)
    text=re.compile(r'\b%s\b' % wed, re.I).sub('wednesday',text)
    text=re.compile(r'\b%s\b' % thu, re.I).sub('thursday',text)
    text=re.compile(r'\b%s\b' % fri, re.I).sub('friday',text)
    text=re.compile(r'\b%s\b' % sat, re.I).sub('saturday',text)
    text=re.compile(r'\b%s\b' % tfl, re.I).sub('transport london',text)
    text=re.compile(r'\b%s\b' % amp, re.I).sub('amplifier',text) 
    return text

def remove_tag(text):
    text=' '.join([letter for letter in text.split() if not len(letter)>=15])
    text=text.lower()
    return text

def meaning_lessWord_remove(text):
    new_sw=sw.words('english')
    new_sw=list(set(new_sw+list(string.ascii_lowercase)))+['much','many','lol','etc','yeah','ummm','haha','omg','hmmm']
    new_sw.remove('not')
    new_text=[]
    for word in text.split():
        if len(word)>2:
            new_text.append(word)
    text=' '.join([word for word in new_text if word not in new_sw])
    return text

def sentence_lemon(text):
        lemon = wn()
        each_lemmon_str = ' '.join([lemon.lemmatize(word) for word in tk(text)])
        allow_postags = set(['NOUN', 'VERB', 'ADJ', 'ADV', 'PROPN'])
        words = []
        for token in nlp(each_lemmon_str):
            if token.pos_ in allow_postags:
                words.append(token.lemma_)
        return ' '.join(words)
    
def data_processing_auto(text):
    result=processed_text=sentence_lemon(
        meaning_lessWord_remove(
            remove_tag(
                single_quote_transfer(
                    emoji_lemon(
                        free_contact(
                            remove_duplicate_emoji(text)))))))
    
    return result

def remove_alpha(text):
    for word in text.split():
        if len(word)>1:
            pattern=re.compile(word)
            poistion=[match.start() for match in pattern.finditer(text)][0]
            text=text[poistion:]
            break
    return text

def remove_meaningless_name(text):
    exclude_words_of_name=sw.words('english')
    new_name=[]
    for word in text.split():
        if word not in exclude_words_of_name:
            new_name.append(word)
    return ' '.join(new_name)
def remove_space(text):
    if len(text)==0:
        text='unknown'
    else:
        if text[0]==' ':
            text=text.lower()[1:]
        else:
            text=text.lower()
    return text

def puntuation_free_text(text):
    tab=str.maketrans(dict.fromkeys(string.punctuation))
    pure_text=text.translate(tab)
    pure_text=''.join([let for let in pure_text if not let.isdigit()])
    return pure_text

def auto_manage(text):
    text=remove_alpha(remove_space(remove_meaningless_name(puntuation_free_text(emoji_free_text(text)))))
    return text                                                  