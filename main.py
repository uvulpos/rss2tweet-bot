import feedparser, dateparser, os, os.path, json, tweepy
from dotenv import load_dotenv
from datetime import datetime, timezone

# load .env file
load_dotenv()

#-------------------------------------------------------------------------------
#       READ / WRITE TIMESTAMP
#-------------------------------------------------------------------------------

def get_last_post_timestamp() -> int:

    current_timestamp = int(datetime.now().timestamp())
    last_post_update = current_timestamp

    current_dir = os.path.dirname(os.path.realpath(__file__)) + "/data.json"

    # read timestamp from file
    try:
        with open(current_dir, "r") as f:
            last_post_update = int(json.loads(f.read())["last_post"])
    except Exception as e:
        pass

    # write timestamp to json file
    with open(current_dir, "w") as f:
        f.write(json.dumps({"last_post": current_timestamp}))

    return last_post_update


#-------------------------------------------------------------------------------
#       TWITTER API AUTHENTIFICATION!
#-------------------------------------------------------------------------------

# authentication of consumer key and secret
auth = tweepy.OAuthHandler(os.getenv("twitter_consumer_key"), os.getenv("twitter_consumer_secret"))

# authentication of access token and secret
auth.set_access_token(os.getenv("twitter_access_token"), os.getenv("twitter_access_token_secret"))
api = tweepy.API(auth)


#-------------------------------------------------------------------------------
#       loop every article
#-------------------------------------------------------------------------------

# fetch all articles by rss feed
all_articles = feedparser.parse(os.getenv("rss_url"))
last_post_timestamp = get_last_post_timestamp()

for article in all_articles["entries"]:

    # fetch article data
    article_name = article["title"]
    article_link = article["link"]
    article_author = article["author"]
    article_timestamp = int(dateparser.parse(article["published"]).timestamp())

    # if article is older than last post -> exit process
    if last_post_timestamp > article_timestamp:
        break

    # author contains name
    if article_author.__contains__(os.getenv("author_contains")):
        # send tweet
        api.update_status(status="Neuer Blogartikel:\n"+article_link)
        print("Neuer Blogartikel:\n"+article_link)
