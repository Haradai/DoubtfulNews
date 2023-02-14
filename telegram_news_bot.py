import asyncio
import telegram
from datetime import datetime
import pickle
import time

TOPICS = ["WORLD", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH"]

group_chatid = "-1001878279558"

TIME_BETWEEN_MSG = 10 #seconds
async def main():
    bot = telegram.Bot("telegra-bot-key")
    async with bot:

        #Send news to each user:

        #get news text
            #printing out the articles:
        for topic in TOPICS:
            try:
                pkl_file = open(f"articles/articles_{topic}.pkl", 'rb')
                articles = pickle.load(pkl_file)
                pkl_file.close()
            except:
                continue
            texts = []
            images = []
            sources = []

            #organizedata from all summaries file
            for artcl in articles:
                texts.append(artcl["text"])
                images.append(artcl["image"])
                sources.append(artcl["sources"])

        
            await bot.send_message(text= '''This is the Questionable Reports bot!🤖
⚠️⚠️ DO NOT SHARE NOR TRUST INFORMATION PROVIDED HERE ⚠️⚠️
This is a mere experiment regarding wether we can use chatGPT + other tools to create a brief news feed from multiple scraped online sources.
Be critic! this is probably in some sense a fake news generator.
''', chat_id=group_chatid)

            await bot.send_message(text= f"-----------\n📅{datetime.today().strftime('%Y-%m-%d')}\n<b>TOPIC:</b> {topic}\n-----------", chat_id=group_chatid,parse_mode='HTML')
            
            for artcl in articles:
                #make sources list as text
                sources_txt = "\n"
                for sourc in artcl["sources"]:
                    sources_txt += sourc + "\n\n"
                #send title, article, image and sources
                await bot.send_message(text= f"<b>{artcl['title']}</b>\n\n{artcl['text']}\n\n <b>Sources:</b> {sources_txt} image:{artcl['image']}", chat_id=group_chatid, parse_mode='HTML')
                time.sleep(TIME_BETWEEN_MSG)
            
if __name__ == '__main__':
    asyncio.run(main())