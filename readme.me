# Doubtful news

This is just a weekend toy project. A proof of concept. The idea was to try implement some sort of articles scraper that using the help of **ChatGPT**, filtered and helped create a summary of many articles talking about the same topic.

To date there isn't any official **ChatGPT** official API, so to interact with it I'm using the unnofficial library [chatgpt-wrapper](https://github.com/mmabrouk/chatgpt-wrapper)

*Note: If you intend to run this code, I'm not exactly using the library as is but instead a fork with function that I wrote to wait for the 60min ChatGPT timeout and other cases when for whatever reason the webpage  it doesn't give a usable answer. [fork](https://github.com/Haradai/chatgpt-wrapper)*

The results of this can be viewed in this [telegram group](https://t.me/DoubtfulDailyNews), reports may not be updated to date as right now I have to run the script manually. I don't have a server with this scheduled to run every morning or something.

## Pipeline
Right now the pipeline is as follows:

Gather top 2 articles from google news using the library [Gnews](https://github.com/ranahaani/GNews) for many topics:  
"WORLD", "BUSINESS", . . . ,"HEALTH"

For each of those articles we get a description that we can feed to **ChatGPT** and ask for: *"Write a search engine text input looking for more articles from multiple sources talking about: " (followed by the description)*

We get then something we can feed to a serach engine, I'm searching **DuckDuckGo** using the library [duckduckgo_search](https://github.com/deedy5/duckduckgo_search)
We can look for 8 more articles like this and then use **ChatGPT** again to filter out by their title if it is relevant or not.  
*"Only answer explicitly with Yes or No. Does the title for an article: '(article title)' suggest to be talking about our search input? Is it the result we want?"*

After that we could try to summarize all articles recursively using **ChatGPT** but for the sake of not doing already too many requests we do the following:

For each article body text  split it into sentences using a pretrained model: [Stanza](https://stanfordnlp.github.io/stanza/), then convert all sentences into vectors using: [sbert](https://www.sbert.net/). Finally kmeans was used to find the "most different in meaning" sentences, bundled up and sent to **ChatGPT** with the purpose of having a coherently written summary of this bundle of sentences.

Finally, with this summaries and keeping tab of the sources used, this is all sent through a **telegram bot** using  [python-telegram-bot](https://github.com/python-telegram-bot)

The results are available at this **telegram group**:
https://t.me/DoubtfulDailyNews . Again, reports may not be updated to date as right now I have to run the script manually.
