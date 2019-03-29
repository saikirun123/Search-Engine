from django.shortcuts import render
from .forms import SearchForm
from .models import Search
from proz.settings import BASE_DIR
from django.http import HttpResponse,HttpResponseForbidden
import os

#IR
import numpy as np
from nltk.corpus import stopwords
from gensim import corpora, models, similarities, matutils
from gensim.models import lsimodel, nmf
from gensim.models.coherencemodel import CoherenceModel 


def home(request):
    return render(request, "home.html")

def LSI(request):
    query = ""
    query_response = None
    file_list = None
    file_list_dictionary = None
    search_result_dictionary = None
    documents = []
    for counter in range(1033):
        temp = open("IR/"+str(counter+1)+".txt", 'r')
        documents.append(temp.read())
        temp.close()
    stop_words = stopwords.words('english')
    texts = [[word for word in document.lower().split() if word not in stop_words] for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]   
    corpora.MmCorpus.serialize('/tmp/ir.mm', corpus)
    lsi = models.LsiModel(corpus,  num_topics=43, id2word = dictionary) 
    if request.method=="POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query_response = list()
            user_query = form.save()
            query = user_query.query
            user_query.save()
            index = similarities.MatrixSimilarity(lsi[corpus])
            doc = user_query.query
            vec_bow = dictionary.doc2bow(doc.lower().split())
            vec_lsi = lsi[vec_bow]
            sims = index[vec_lsi]
            sims = sorted(enumerate(sims,1), key=lambda item: -item[1])
            file_list = list()
            for element in sims[0:5]:
                file_list.append(element[0])
            temp = None
            for text in file_list:
                temp = open("IR/"+str(text)+".txt", 'r')
                query_response.append(temp.read())
                temp.close()
            #print(query_response)
            file_list_dictionary = dict()
            file_list_dictionary = { i : file_list[i-1] for i in range(1, len(file_list)+1) }
            search_result_dictionary = { i : query_response[i-1] for i in range(1, len(query_response)+1) }
    else:
        form = SearchForm()    
    return render(request, "lsi.html", {'form':form, 'query':query, 'answer':file_list, 'search_results':query_response, 'file_dictionary':file_list_dictionary, 'search_result_dictionary':search_result_dictionary})

def NMF(request):
    query = ""
    query_response = None
    file_list = None
    file_list_dictionary = None
    search_result_dictionary = None
    documents = []
    for counter in range(1033):
        temp = open("IR/"+str(counter+1)+".txt", 'r')
        documents.append(temp.read())
        temp.close()
    stop_words = stopwords.words('english')
    texts = [[word for word in document.lower().split() if word not in stop_words] for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]   
    corpora.MmCorpus.serialize('/tmp/ir.mm', corpus)
    nmfmodel = nmf.Nmf(corpus, num_topics=43, id2word = dictionary, normalize =True)
    if request.method=="POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query_response = list()
            user_query = form.save()
            user_query.save()
            query = user_query.query            
            doc = user_query.query
            index = similarities.MatrixSimilarity(nmfmodel[corpus])
            vec_bow = dictionary.doc2bow(doc.split())
            vec_nmf = nmfmodel[vec_bow]        
            sims = index[vec_nmf]
            sims = sorted(enumerate(sims,1), key=lambda item: -item[1])
            file_list = list()
            for element in sims[0:5]:
                file_list.append(element[0])
            temp = None
            for text in file_list:
                temp = open("IR/"+str(text)+".txt", 'r')
                query_response.append(temp.read())
                temp.close() 
            #print(query_response)
            file_list_dictionary = dict()
            file_list_dictionary = { i : file_list[i-1] for i in range(1, len(file_list)+1 ) }
            search_result_dictionary = { i : query_response[i-1] for i in range(1, len(query_response)+1) }
    else:
        form = SearchForm()
    return render(request, "nmf.html", {'form':form,'query':query, 'answer':file_list, 'search_results':query_response, 'file_dictionary':file_list_dictionary, 'search_result_dictionary':search_result_dictionary})