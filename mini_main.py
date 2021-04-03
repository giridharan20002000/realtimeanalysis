# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 19:51:04 2020

@author: LENOVO
"""
from __future__ import print_function
import re
import wikipediaapi
from flask_sqlalchemy import SQLAlchemy

import requests
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import matplotlib.pyplot as plt
import time
# Data to plot
from flask import Flask
from flask import render_template,request
app = Flask(__name__)
import os
from bs4 import BeautifulSoup
import wikipedia
from search_web import *
from pytrends.request import TrendReq
import json
import urllib
title,url1,desp,source,wiki=[],[],[],[],[]
newtitle,newurl,newdesp,newsource=[],[],[],[]


pos=''
neg=''

i=0
path="C:/Users/LENOVO/gir/static/images/new_plot"
searchtweet=None
ptweets=None
ntweets=None
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'YqtlRlUVUpbi9A9W037olterL'
        consumer_secret = 'xScHDi93BcvKuRd3qNpuEprLrYZ19wYxgzLcn6ZYFTU9XfBnzt'
        access_token = '1214197576762716162-3gNU5hGDT7SRBFlK8BBjtajP1vUTez'
        access_token_secret = 'pFwwYv5tCAGPqfM8FiH5OeOenSz1qhBo8upY17VKVZnTB'

        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
                                

    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet))
        
        
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 

        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 

            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 

                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 

            # return parsed tweets 
            return tweets 

        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
def callwebsite():
    
    return render_template('show_plot.html', name = 'new_plot')
    
@app.route('/home')
def main1(): 
    # creating object of TwitterClient Class 
    
    global searchtweet,pos,neg,ptweets,ntweets,det,imag
    global title,url1,desp,source,wiki
    
    print(os.getcwd(),"is the current os path")
    api = TwitterClient() 
    # calling function to get tweets 
    e=searchtweet
    print(e,"is the search tweet.")
    tweets = api.get_tweets(query = e, count = 100) 

    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 
        
    # printing first 5 positive tweets 
     
    for tweet in ptweets[:4]:
        
        pos=pos+tweet['text']+'\n\n\n'
    
 

    pos=pos+'\n\n\n\n\n\n\n\n\n\n\n\n'
     
    for tweet in ntweets[:4]:
        neg=neg+tweet['text']+'\n\n\n'
        
    


    # Data to plot
    labels = 'Postive commands', 'negative commands', 'netural commands', 
    sizes = [len(ptweets),len(ntweets),(len(tweets)-len(ptweets)-len(ptweets))]
    colors = ['gold', 'yellowgreen', 'lightcoral']
    explode = (0, 0.1, 0)  # explode 1st slice
    print("plot is printed")
    '''rew='https://www.bing.com/search?q='+searchtweet
    r = requests.get(rew)
    
    soup = BeautifulSoup(r.text)
    le=soup.select('a')
    print(le)'''
    """Example of Python client calling Knowledge Graph Search API."""
   
    
    '''api_key = open('.api_key').read()
    query = 'Taylor Swift'
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    for element in response['itemListElement']:
      print(element['result']['name'] + ' (' + str(element['resultScore']) + ')')'''
    """"wiki_wiki = wikipediaapi.Wikipedia('en')

    page_py = wiki_wiki.page(searchtweet)
    print("Page - Exists: %s" % page_py.exists())
    
    print("Page - Title: %s" % page_py.title)
    # Page - Title: Python (programming language)

    print("Page - Summary: %s" % page_py.summary[0:60])"""
    

    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"
    
    querystring = {"q":searchtweet,"pageNumber":"1","pageSize":"10","autoCorrect":"true"}
    
    headers = {
        'x-rapidapi-key': "6bb21d3951msh6538f6955afebb0p16190ejsndbc4aefc68c9",
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
        }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    i=response.text.find("url")+6
    j=i
    while(response.text[i]!="\""):
        i+=1
    imag=response.text[j:i]
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"

    querystring = {"q":searchtweet,"pageNumber":"1","pageSize":"10","autoCorrect":"true","fromPublishedDate":"null","toPublishedDate":"null"}

    headers = {
    'x-rapidapi-key': "6bb21d3951msh6538f6955afebb0p16190ejsndbc4aefc68c9",
    'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    s=response.text

    


    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"
    queryst=searchtweet+" wikipedia"
    
    querystring = {"q":queryst,"pageNumber":"1","pageSize":"10","autoCorrect":"true"}
    
    headers = {
        'x-rapidapi-key': "6bb21d3951msh6538f6955afebb0p16190ejsndbc4aefc68c9",
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
        }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    wik=response.text
    print("resource fetched")
    u=0
    stat=0
    for num in range(0,3):
        print("num:",num)
        
        t1=s.find("title",stat)
        j=t1+8
        i=j
        while(s[i]!="\""):
                i+=1
        print("first title is over")
        title.append(s[j:i])
        t2=s.find("url",stat)
        j=t2+6
        i=j
        
        while(s[i]!="\""):
                i+=1
        
        url1.append(s[j:i])
        
        t3=s.find("description",stat)
        j=t3+14
        i=j
        
        iop=s.find("\"keywords\"",i)
        print("iop",iop)
        while(i!=iop):
                i+=1
                
        
        desp.append(s[j:i])
        # initializing sub list 
        sub_list = ["\\", "\\n","\"","body",":"]
          
        # Remove substring list from String
        # Using loop + replace()
        
        desp[num]=desp[num].replace("\n"," ")
        
            
        t4=s.find("\"provider\":{\"name\":",stat)
        
        j=t4+20
        i=j
        
        
        while(s[i]!="\""):
                i+=1
                
        
        source.append(s[j:i])
        
        stat=s.find("{\"id\":\"",i)
        
    
    t3=wik.find("description")
    j=t3+14
    i=j
    iop=wik.find("body")
    while(i!=iop or j-1==100000):
        i+=1
        
    wiki.append(wik[j:i])
    
    

    
    
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')
    #det=wikipedia.summary(searchtweet, sentences=2)
    det=""
    
    plt.savefig("C:/Users/LENOVO/gir/static/images/new_plot0.png",dpi=100)
    
    plt.show()
    
    plt.close()
    

        
@app.route('/proceed',methods = ['POST', 'GET'])
def main2():
    
    global searchtweet,ptweets,ntweets
    searchtweet=request.form['search']
    
    main1()
    
    return render_template('templates/hello.html', postive=ptweets,negative=ntweets,d=searchtweet,img=imag,wik=wiki[0],news1=title[0],new1des=desp[0],newsou1=source[0],url1=url1[0],news2=title[1],new2des=desp[1],newsou2=source[1],url2=url1[1],news3=title[2],new3des=desp[2],newsou3=source[2],url3=url1[2])
@app.route('/trends',methods = ['POST', 'GET'])
def main4():
    idi=0,
    ihip=0
    ts={}
    di={}
    dip={}
    dip[1] = {}
    dip[2] = {}
    dip[3] = {}
    dip[0] = {}
    dip[4] = {}
    dip[5] = {}
    dip[6] = {}
    ps={}
    hip={}
    hip[1]={}
    hip[2]={}
    hip[3]={}
    hip[0]={}
    hip[4]={}
    hip[5]={}
    hip[6]={}
    global newtitle,newurl,newdesp,newsource,api
    ser=[]
    '''url = "https://bing-news-search1.p.rapidapi.com/news/trendingtopics"

    querystring = {"textFormat":"Raw","safeSearch":"Off"}

    headers = {
    'x-bingapis-sdk': "true",
    'x-rapidapi-key': "6bb21d3951msh6538f6955afebb0p16190ejsndbc4aefc68c9",
    'x-rapidapi-host': "bing-news-search1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)'''



    
    
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=in&'
       'apiKey=284fdc349e0e4642a25cae0a848ed173')
    response = requests.get(url)
    res=response.json()
    
    for i in res['articles']:
        newtitle.append(i['title']),newsource.append(i["source"]["name"]),newurl.append(i['url']),newdesp.append(i['description'])
    pytrends = TrendReq(hl='en-IN', tz=360, timeout=(10,25),  retries=2, backoff_factor=0.1)
    trends_searches=pytrends.trending_searches(pn='india')
    ps=trends_searches.to_dict()
    l=0
    idip=0
    while(l<16):
        if(l%3==0):
            idip+=1
        dip[idip][l]=ps[0][l]
        l=l+1
   
    
    
        
        
    
    
    print("list",trends_searches.shape)
    consumer_key = 'YqtlRlUVUpbi9A9W037olterL'
    consumer_secret = 'xScHDi93BcvKuRd3qNpuEprLrYZ19wYxgzLcn6ZYFTU9XfBnzt'
    access_token = '1214197576762716162-3gNU5hGDT7SRBFlK8BBjtajP1vUTez'
    access_token_secret = 'pFwwYv5tCAGPqfM8FiH5OeOenSz1qhBo8upY17VKVZnTB'

        # attempt authentication 
    try: 
            # create OAuthHandler object 
        auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
        auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
        api = tweepy.API(auth) 
    except: 
            print("Error: Authentication Failed") 
    di=api.trends_place(2459115)
    
    
    for i in range(3):
        hip[ihip][di[0]['trends'][i]['name']]=di[0]['trends'][i]['url']
    ihip=1
    for i in range(3,6):
        hip[ihip][di[0]['trends'][i]['name']]=di[0]['trends'][i]['url']
    ihip=2
    for i in range(6,9):
        hip[ihip][di[0]['trends'][i]['name']]=di[0]['trends'][i]['url']
    ihip=3
    for i in range(9,12):
        hip[ihip][di[0]['trends'][i]['name']]=di[0]['trends'][i]['url']
    return render_template('templates/trends.html',news1=newtitle[0],new1des=newdesp[0],newsou1=newsource[0],url1=newurl[0],news2=newtitle[1],new2des=newdesp[1],newsou2=newsource[1],url2=newurl[1],news3=newtitle[2],new3des=newdesp[2],newsou3=newsource[2],url3=newurl[2],hip0=hip[0],hip1=hip[1],hip2=hip[2],hip3=hip[3],dip0=dip[0],dip1=dip[1],dip2=dip[2],dip3=dip[3])
    
    
   
@app.route('/')
def main3():
    return render_template('templates/update.html')
    

if __name__ == "__main__": 
    # calling main function
    
    
    app.run()

