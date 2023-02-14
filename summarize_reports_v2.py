import glob #list files in directory
import pandas as pd #dataframe handling
from tqdm import tqdm#show nice progress bar of iterables
import stanza #wrapper for model that splits text into sentences
from chatgpt_wrapper import ChatGPT #wrapper for chatGPT so we can have our summarization done
from sentence_transformers import SentenceTransformer #sentence to vector -> used to compare sentences by their semantic meaning

#these are used to look for similar sentences
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np

import pickle as pkl


TOPICS = ["WORLD", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH"]

CHUNKSIZE = 15 #constant used for the number of sentences size of the text passed to chat gpt
NSENTENCES = 30

#range in seconds, sleep randomly between 
MINTIME = 5
MAXTIME = 10

#create stanza object used to split text into sentences
text_to_sentence = stanza.Pipeline('en', processors='tokenize')

#initialize chatgpt chat
bot = ChatGPT()

#create object to compare semantically sentences
sntc2vec = SentenceTransformer('all-MiniLM-L6-v2')

print("Summarizing reports...")
for topic in TOPICS:
    print(f"Processing {topic}")
    list_of_files = glob.glob(f"topic_csv/{topic}/*.csv") #get paths of csv files to process
    articles = []
    for pth in tqdm(list_of_files,desc="Processing articles"): #iterate all files in folder
        #time.sleep(60*10) #sleep 10minites between articles, for sake of chatgpt
        tree = pd.read_csv(pth) #read reports list in csv
        raw_sentences = [] #store here list of summary sentences generated for each article
        bot.new_conversation() #restart a new clean chat
        for i,row in tree.iterrows(): #iterate each report
            initial_raw_sum = [] #we'll store here the output of each iteration of chatgpt
            sentences = [sntc.text for sntc in text_to_sentence.process(row["text"]).sentences] #get list of sentences
            raw_sentences += sentences

        raw_vects = sntc2vec.encode(raw_sentences) #convert all sentences to vectors

        #check if the number of samples we have is bigger than the number of klusters we want to look for,
        #otherwise just use everything we got(the norm should be to not)
        if(len(raw_vects) > NSENTENCES):
            #Use kmeans to find most relevant sentences
            kmeans = KMeans(n_clusters=NSENTENCES).fit(raw_vects) 
            #indexes where the vectors are closest to each kcenters
            closest_tokcent, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, raw_vects)
        else:
            closest_tokcent =  np.arange(len(raw_vects))#later when using this as indexes will basically get all sentences we have


        
        #not the best way but fast enough
        #clump together the selected sentences
        article = ""
        for idx in list(closest_tokcent):
            article += raw_sentences[idx]
        
        #Use chatGpt again on the same chat to ask for the new generated article
        new_article = {}
        new_article["text"] = bot.consistent_ask('''Write a very brief 100 word newspaper article summary connecting and precisely referncing the following portrayed ideas, avoid any publicitary information:
        '''+article)
        #generate a title for it
        new_article["title"] = bot.consistent_ask("Answer with the title of the article.")
        new_article["image"] = tree["top_image"][0] #get the first image of the root article
        new_article["sources"] = list(tree["url"])
        articles.append(new_article)

    #save to pickle each time just in case
    output = open(f"articles/articles_{topic}.pkl","wb")
    pkl.dump(articles,output)
    output.close()