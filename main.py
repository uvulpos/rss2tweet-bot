import feedparser, dateparser, os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

# fetch all articles by rss feed
all_articles = feedparser.parse(os.getenv("rss_url"))

# loop every article
for article in all_articles["entries"]:

    # fetch article data
    article_name = article["title"]
    article_link = article["link"]
    article_timestamp = int(dateparser.parse(article["published"]).replace(tzinfo=timezone.utc).timestamp())

    # print article to console
    print("- ", article_timestamp, " ", article_name, " ", article_link)
