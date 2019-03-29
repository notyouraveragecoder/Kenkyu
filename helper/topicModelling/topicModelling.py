import pdftotext
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import spacy
import os
import numpy as np
import pandas as pd
# from tqdm import tqdm
import string
# import matplotlib.pyplot as plt
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
import concurrent.futures
import time
# import pyLDAvis.sklearn
# from pylab import bone, pcolor, colorbar, plot, show, rcParams, savefig
# import warnings
# warnings.filterwarnings('ignore')

# %matplotlib inline
# print(os.listdir("../input"))

# Plotly based imports for visualization
# from plotly import tools
# import plotly.plotly as py
# from plotly.offline import init_notebook_mode, iplot
# init_notebook_mode(connected=True)
# import plotly.graph_objs as go
# import plotly.figure_factory as ff

# spaCy based imports
nlp = spacy.load('en')


class GetTopics():
    def spacy_tokenizer(self, sentence):
        mytokens = parser(sentence)
        mytokens = [word.lemma_.lower().strip() if word.lemma_ !=
                    "-PRON-" else word.lower_ for word in mytokens]
        mytokens = [
            word for word in mytokens if word not in stopwords and word not in punctuations]
        mytokens = " ".join([i for i in mytokens])
        return mytokens

    def selected_topics(self, model, vectorizer, top_n=10):
        topic_list = []
        for idx, topic in enumerate(model.components_):
            # print("Topic %d:" % (idx))
            for i in topic.argsort()[:-top_n - 1:-1]:
                topic_word = vectorizer.get_feature_names()[i]
                if topic_word not in topic_list:
                    topic_list.append(topic_word)
        return topic_list

    def getTopics(self, pdf):
        pdf_processed = []
        for page in pdf:
            pdf_processed.append(self.spacy_tokenizer(page))
        # print(pdf_processed)
        vectorizer = CountVectorizer(min_df=5, max_df=0.9, stop_words='english',
                                     lowercase=True, token_pattern='[a-zA-Z\-][a-zA-Z\-]{2,}')
        data_vectorized = vectorizer.fit_transform(pdf_processed)

        NUM_TOPICS = 2

        lda = LatentDirichletAllocation(
            n_components=NUM_TOPICS, max_iter=10, learning_method='online', verbose=False)
        data_lda = lda.fit_transform(data_vectorized)
        topic_list = self.selected_topics(lda, vectorizer)
        return topic_list


punctuations = string.punctuation
stopwords = list(STOP_WORDS)
parser = English()

with open("vgg.pdf", "rb") as f:
    pdf_one = pdftotext.PDF(f)
pdf_one_topic_list = GetTopics().getTopics(pdf_one)

with open("random.pdf", "rb") as f:
    pdf_two = pdftotext.PDF(f)
pdf_two_topic_list = GetTopics().getTopics(pdf_two)

list3 = set(pdf_one_topic_list) & set(pdf_two_topic_list)

common_topics = sorted(list3, key=lambda k: pdf_one_topic_list.index(k))
print(len(common_topics)/(len(pdf_one_topic_list) + len(pdf_two_topic_list)))
print(common_topics, len(pdf_one_topic_list), len(pdf_two_topic_list))
