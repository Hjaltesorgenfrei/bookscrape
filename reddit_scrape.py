import datetime
import sqlite3
import time
import requests

# open sqlite database
conn = sqlite3.connect('reddit.db')
# create a table in the database for posts
def create_table():
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS posts (id TEXT primary key, title TEXT, author TEXT, created_utc INTEGER, score INTEGER, num_comments INTEGER, permalink TEXT, url TEXT, over_18 INTEGER, domain TEXT, subreddit TEXT, selftext TEXT)")
    conn.commit()

# use pushshift.io to get every submission from a subreddit
def get_submissions(subreddit, end, count = 1000):
    url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={str(count)}&before={str(end)}"
    print(f"Getting {url}")
    r = requests.get(url)
    return r.json()['data']


create_table()
end = int(time.time())
results = []
while True:
    result = get_submissions('HFY', end)
    if result == []:
        break
    results += result
    end = result[-1]['created_utc']
    # sleep for 1 second to avoid rate limiting
    time.sleep(1)
    # insert the posts into the database
    c = conn.cursor()
    to_insert = []
    for post in result:
        # check if keys are in the post
        if 'id' in post and 'title' in post and 'author' in post and 'created_utc' in post and 'score' in post and 'num_comments' in post and 'permalink' in post and 'url' in post and 'over_18' in post and 'domain' in post and 'subreddit' in post and 'selftext' in post:
            to_insert.append((post['id'], post['title'], post['author'], post['created_utc'], post['score'], post['num_comments'], post['permalink'], post['url'], post['over_18'], post['domain'], post['subreddit'], post['selftext']))
        else:
            print("Missing key in post")
            print(post)
    c.executemany("INSERT OR IGNORE INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", to_insert)
    conn.commit()

print("Done")