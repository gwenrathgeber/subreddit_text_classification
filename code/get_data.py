import requests
import time
import pandas as pd
import sys 

# Set list of subreddits to crawl
subs = ['asoiaf','freefolk','gameofthrones']

# Set number of days of data to gather
try:
    days = int(sys.argv[1])
except:
    days = int(input('Please enter the number of days you would like to crawl: '))

# Set API base url (no key needed)
base_url =  'https://api.pushshift.io/reddit/'

# Function to make an individual Pushshift API request
# Returns dictionary of the .json API response
def request_posts(subreddit, days_ago, base_url=base_url, 
                  endpoint='search/submission/', is_video='is_video=false'):
    try:    
        response = requests.get(f'{base_url}{endpoint}?subreddit={subreddit}&{is_video}&before={days_ago}d&after={days_ago+1}d&size=1000')
        assert response.status_code == 200
    except:
        pass
    
    return response

# Function to make n requests of 100 posts from n days
# Returns dataframe of API responses from a subreddit
def make_requests(subreddit, days_of_data):
    all_results = []
    
    for i in range(1, days_of_data):
        try:
            entry = request_posts(subreddit,i)
            all_results.append(pd.DataFrame(entry.json()['data']))
        except:
            pass
        if i % 100 == 0:
            print(f'{i} of {days_of_data} requests completed')
        time.sleep(1.5)
        
    return pd.concat(all_results)

# Function to make n requests of 100 posts from n days over m subreddits
# Returns dataframe of API responses from all subreddits
def request_all_subs(list_of_subreddits, days_of_data):
    all_results = []
    for sub in list_of_subreddits:
        print(f'Querying {sub}...')
        sub_df = make_requests(sub,days_of_data)
        all_results.append(sub_df)
    return pd.concat(all_results)

# Executes all requests for n days of data across the subreddits list and writes results to a .csv
def main(days=days):
    df = request_all_subs(subs,days)
    df.to_csv('../data/subreddit_data.csv', index=False)

if __name__ == "__main__":
    main()