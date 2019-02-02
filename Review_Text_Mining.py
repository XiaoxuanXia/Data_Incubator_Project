#!/usr/bin/env python
# coding: utf-8

# In[80]:


get_ipython().system('pip install wordcloud')
get_ipython().system('pip install vaderSentiment')
get_ipython().system('pip install gensim')
get_ipython().system('pip install pyLDAvis')

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import inaugural
from nltk import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import collections
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import OrderedDict
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
import pyLDAvis.gensim
import pprint
import re
import warnings
warnings.filterwarnings('ignore')


# In[109]:


def Reviews_Text_Analysis(year):
    content_list = []
    audience_list = []
    critic_list = []
    
    #Read data
    path = ""
    with open(path + 'audience_review_%s.txt' % str(year),'r') as f:
        audience_review = f.read().strip().lower()
    audience_review = re.sub("[\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。:|？、~@#￥%……&*（）]+","",audience_review)
    with open(path + 'critic_review_%s.txt' % str(year),'r') as f:
        critic_review = f.read().strip().lower()
    critic_review = re.sub("[\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。:|？、~@#￥%……&*（）0-9]+","",critic_review)
    critic_review = re.sub(r"full review | original score","",critic_review)
    
    #Sentiment Analysis
    content_list.extend(['Sentiment Analysis-Pos/Neg Percentage','Sentiment Analysis-Emotion Percentage'])
    x = sentiment(audience_review)
    audience_list.extend([x[0],x[1]])
    y = sentiment(critic_review)
    critic_list.extend([y[0],y[1]])
    
    #Words frequency
    def frequency(text):
        import collections
        counter = collections.Counter(text.split())

        from nltk.corpus import stopwords
        #Do some cleaning for wordcloud and topic analysis
        #Remove some general words which matter little when doing topic analysis
        general_set = set(['.',',','-','_',''
                        'movie','movies','film','one','really','see','much','even'])
        stops = set(stopwords.words('english')) | general_set
        counts = [(word, count) for word, count in counter.most_common() 
                  if word not in stops]
        return counts
    content_list.append('Top Word Frequency')
    fre1 = frequency(audience_review)
    fre2 = frequency(critic_review)
    str1 = "%s(%s) "%(fre1[0][0],str(fre1[0][1])) + "%s(%s) "%(fre1[1][0],str(fre1[1][1])) + "%s(%s) "%(fre1[2][0],str(fre1[2][1])) + "%s(%s) "%(fre1[3][0],str(fre1[3][1])) + "%s(%s)"%(fre1[4][0],str(fre1[4][1]))
    str2 = "%s(%s) "%(fre2[0][0],str(fre1[0][1])) + "%s(%s) "%(fre2[1][0],str(fre1[1][1])) + "%s(%s) "%(fre2[2][0],str(fre1[2][1])) + "%s(%s) "%(fre2[3][0],str(fre1[3][1])) + "%s(%s)"%(fre2[4][0],str(fre1[4][1]))
    audience_list.append(str1)
    critic_list.append(str2)

    #Calculate the complexity
    from nltk.corpus import inaugural
    from nltk import sent_tokenize, word_tokenize
    content_list.append('Complexity Statistics')
    def get_complexity(text):
        num_chars=len(text)
        num_words=len(word_tokenize(text))
        num_sentences=len(sent_tokenize(text))
        vocab = {x.lower() for x in word_tokenize(text)}
        return len(vocab),int(num_chars/num_words),len(vocab)/num_words
    #(vocab,word_size,sent_size,vocab_to_text) 
    comp1 = get_complexity(audience_review)
    comp2 = get_complexity(critic_review)
    comp_str1 = "Vocabulary num:{0:1.2f} Avg. Word Size:{1:1.2f} Unique Word Percentage:{2:1.2f}%".format(comp1[0],comp1[1],comp1[2])
    comp_str2 = "Vocabulary num:{0:1.2f} Avg. Word Size:{1:1.2f} Unique Word Percentage:{2:1.2f}%".format(comp2[0],comp2[1],comp2[2])
    audience_list.append(comp_str1)
    critic_list.append(comp_str2)
    
    #Get stemming amd dispersion plot
    def dispersion_plot(text,targets):
        #Get stemming amd dispersion plot
        from nltk.stem.porter import PorterStemmer
        p_stemmer = PorterStemmer()
        striptext = text.replace('\n\n', ' ')
        striptext = striptext.replace('\n', ' ')
        sentences = sent_tokenize(striptext)
        words = word_tokenize(striptext)
        text = nltk.Text([p_stemmer.stem(i).lower() for i in words])
        text.dispersion_plot([targets[0], targets[1], targets[2], targets[3]])
    targets = ['good','bad','cast','story','pace']
    print('\n\n\nAudience Reviews Dispersion Plot')
    dispersion_plot(audience_review,targets)
    print('\n\n\nCritic Reviews Dispersion Plot')
    dispersion_plot(critic_review,targets)

    #Topic Modeling
    print("\n\n\nLDA Topic Modeling Results:\n")
    def LDA_topic_modeling(text):
        #prepare the text
        non_topic_set = set(['.',',','-','_',''
                            'movie','movies','film','one','really','see','much','even','good','great','bad','characters'])
        new_set = STOPWORDS | non_topic_set
        sents = sent_tokenize(text)
        for j in range(len(sents)):
            sent = sents[j]
            sent = sent.strip().replace('\n','').replace('.', '')
            sents[j] = sent
        text = '. '.join(sents)
        texts = [[word for word in text.lower().split() if word not in new_set and word.isalnum() and not word.lower() == 'slate']]
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts] #(word_id,freq) pairs by sentence
        #set the parameters
        num_topics = 5 #The number of topics that should be generated
        passes = 10 #More passes, slower analysis
        lda = LdaModel(corpus,
                  id2word=dictionary,
                  num_topics=num_topics,
                  passes=passes)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(lda.print_topics(num_words=8))
        return lda, corpus, dictionary
    print("\n\tAudience Reviews Topic Modeling:\n\n")
    lda1,corpus1,dictionary1 = LDA_topic_modeling(audience_review)
    print("\n\tCritic Reviews Topic Modeling:\n\n")
    lda2,corpus2,dictionary2 = LDA_topic_modeling(critic_review)
    lda_display1 = pyLDAvis.gensim.prepare(lda1, corpus1, dictionary1, sort_topics=False)
    lda_display2 = pyLDAvis.gensim.prepare(lda2, corpus2, dictionary2, sort_topics=False)
    pyLDAvis.display(lda_display1)
    pyLDAvis.display(lda_display2)
    
    
    #Draw and save the word cloud
    get_ipython().run_line_magic('matplotlib', 'inline')
    wordcloud1 = WordCloud(stopwords=STOPWORDS,background_color='white').generate(audience_review)
    wordcloud2 = WordCloud(stopwords=STOPWORDS,background_color='white').generate(critic_review)
    plt.imshow(wordcloud1)
    plt.axis('off')
    plt.title('Audience Word Cloud')
    plt.savefig("audience_word_cloud.png")
    plt.show()
    plt.imshow(wordcloud2)
    plt.axis('off')
    plt.title('Critic Word Cloud')
    plt.savefig("critic_word_cloud.png")
    

    #Create data frame
    df = pd.DataFrame({'Content of Analysis':content_list,'Audience Review':audience_list,'Critic Review':critic_list})
    df.set_index(['Content of Analysis'], inplace=True)
    pd.set_option('max_colwidth', 200)
    return df
    


# In[110]:


Reviews_Text_Analysis(2016)

