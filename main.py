import feedparser, dateparser, os, os.path, json, tweepy
from dotenv import load_dotenv
from datetime import datetime, timezone

# load .env file
load_dotenv()

# get timestamp from lst post
def get_last_post_timestamp() -> int:

    # set default values
    last_post_update = 0
    current_timestamp = int(datetime.now().timestamp())

    # get path to data json file
    current_dir = os.path.dirname(os.path.realpath(__file__)) + "/data.json"

    # if exists -> read data, if fail -> override file
    if os.path.isfile(current_dir):
        try:
            with open(current_dir, "r") as f:
                last_post_update = int(json.loads(f.read())["last_post"])
        except Exception as e:
            pass

    # update last post timestamp
    with open(current_dir, "w") as f:
        f.write(json.dumps({"last_post": current_timestamp}))

    # if error or first execution set timestamp to now
    if last_post_update == 0:
        last_post_update = current_timestamp

    return last_post_update


# fetch all articles by rss feed
all_articles = feedparser.parse(os.getenv("rss_url"))
last_post_timestamp = get_last_post_timestamp()

#
#       TWITTER API AUTHENTIFICATION!
#

# authentication of consumer key and secret
auth = tweepy.OAuthHandler(os.getenv("twitter_consumer_key"), os.getenv("twitter_consumer_secret"))

# authentication of access token and secret
auth.set_access_token(os.getenv("twitter_access_token"), os.getenv("twitter_access_token_secret"))
api = tweepy.API(auth)


#
#       loop every article
#

for article in all_articles["entries"]:

    # fetch article data
    article_name = article["title"]
    article_link = article["link"]
    article_timestamp = int(dateparser.parse(article["published"]).timestamp())

    # if article is older than last post -> exit process
    if last_post_timestamp > article_timestamp:
        break



    # send tweet
    api.update_status(status="Neuer Blogartikel:\n"+article_link)
    print("Neuer Blogartikel:\n"+article_link)
