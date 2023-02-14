import pandas as pd
from gnews import GNews
from newspaper import Article
from tqdm import tqdm
from duckduckgo_search import ddg_news
import os
from datetime import datetime
from chatgpt_wrapper import ChatGPT
import time



TOPICS = ["WORLD", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH"]

def df_search_articles_bytopic(topic:str,exclude_websites:list,language='en', period='7d', max_results=10) -> pd.DataFrame : 
    #create GNews search object and perform search
    gnews_obj = GNews(language='en', period='7d', max_results=25, exclude_websites=exclude_websites) #get a lot of news so that if we are unable to access one we already have more loaded
    world_news = gnews_obj.get_news_by_topic(topic)
    
    #create empty df
    articles = pd.DataFrame(columns = ["url","publisher","description","pub_date","title","text","authors","top_image","movies"])
    for i, new_obj in tqdm(enumerate(world_news[:max_results]),total=max_results):
        article = Article(world_news[i]["url"])
        failed_bool =  True
        cnt = 0
        while failed_bool == True:
            cnt += 1 #look deeper each time into the news output
            try:
                article.download()
                article.parse()
                if len(article.text) == 0:
                    print("can't get text: ",world_news[i]["url"])
                    failed_bool = True
                else:
                    data = {"url":new_obj["url"],"publisher":new_obj["publisher"]["href"],"description":new_obj["description"],"pub_date":new_obj["published date"],"title":new_obj["title"],"text":article.text,"authors":article.authors,"top_image":article.top_image,"movies":article.movies}
                    articles.loc[len(articles)] = data
                    failed_bool =  False
            except:
                print("failed downloading: ",world_news[i]["url"])
                failed_bool = True

            #if failed look for another one
            if(failed_bool == True):
                print("looking for another one...")
                article = Article(world_news[-cnt]["url"])
                world_news.pop(-cnt) #make the last one not accessible again by other failing source
    
    return articles


def df_expand_search_articles(root_article:pd.Series,max_results=10,polite_wait=5) -> pd.DataFrame : 
    
    #we are going to make a search using duck duck go, to get better results we'll get chat
    #gpt to summarize our root article description into a promp for text search.
    bot.new_conversation() #restart a new clean chat
    input = "Write a search engine text input looking for more articles from multiple sources talking about: "+root_article["description"]
    search_title = bot.consistent_ask(input)
    print(search_title)
    #search articles using duckduckgo
    #Note: having the output of chatgpt be within "" and passing that text as a string to the duckduckgo library
    #messes with it and returns nothing. So removing that.
    search_title = search_title.replace('"','')
    result = ddg_news(search_title, region='wt-wt', safesearch='Off', time='w', max_results=max_results)
    #create empty df
    articles = pd.DataFrame(columns = ["url","publisher","description","pub_date","title","text","authors","top_image","movies"])
    
    #add root article
    articles.loc[len(articles)] = root_article

    for i, new_obj in tqdm(enumerate(result),total=len(result)):
        time.sleep(polite_wait) #some polite waiting between requests to chatgpt, in seconds
        
        #check if the article found is the same as the root one 
        if(new_obj["title"] != root_article["title"]):
            #We'll again use chatgpt to better filter our searches,
            #we'll filter if the found article talks or not about the topic we have at hand.
            input = f"Only answer explicitly with Yes or No. Does the title for an article: '{new_obj['title']}' suggest to be talking about our search input? Is it the result we want?"
            gpt_judge = bot.consistent_ask(input)
            if (gpt_judge != "No."): #otherwise yes, to avoid chatgpt not behaving, just in case :)
                article = Article(result[i]["url"])
                try:
                    article.download()
                    article.parse()
                    if len(article.text) == 0:
                        print("can't get text: ",result[i]["url"])
                    else:
                        data = {"url":new_obj["url"],"publisher":new_obj["source"],"description":new_obj["body"],"pub_date":new_obj["date"],"title":new_obj["title"],"text":article.text,"authors":article.authors,"top_image":article.top_image,"movies":article.movies}
                        articles.loc[len(articles)] = data
                except:
                    print("failed downloading: ",result[i]["url"])
            
    return articles

#Archiving old articles and preparing folders for new to process
os.system(f"mkdir archive archive/{datetime.today().strftime('%Y_%m_%d')}")
os.system(f"mv topic_csv archive/{datetime.today().strftime('%Y_%m_%d')}")
os.system(f"mv articles archive/{datetime.today().strftime('%Y_%m_%d')}")

#creating clean folder tree to work on
folders_paths = ""
for topic in TOPICS:
    folders_paths += " topic_csv/"+topic
os.system("mkdir topic_csv articles"+folders_paths)

bot = ChatGPT()

for topic in TOPICS:
    print(f"Processing {topic}...")
    print("-->Gathering root articles...")
    root_articles = df_search_articles_bytopic(topic = topic,max_results=2,exclude_websites=["www.youtube.com"])
    #for each article found for that topic find more articles
    print("-->Scraping expanded articles...")
    for i, article in root_articles.iterrows():
        tree = df_expand_search_articles(article,max_results=8).to_csv(f"topic_csv/{topic}/subtree{i}.csv",index=False)
