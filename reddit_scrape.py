import datetime
import requests

# use pushshift.io to get every submission from a subreddit
def get_submissions(subreddit, end):
    url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size=1&before={str(end)}"
    r = requests.get(url)
    return r.json()['data']


end = int(datetime.datetime.now().timestamp())
for i in range(5):
    result = get_submissions('python', end)
    print(result)
    end = result[-1]['created_utc']