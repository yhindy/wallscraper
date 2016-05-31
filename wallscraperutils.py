"""
This module contains methods that are useful for 
the wallscraper.py module.
"""

import requests
import time

baseurl = 'https://www.reddit.com/r/'

def query(subreddit):
    """
    This functions takes a subreddit and returns the
    json data by using the requests library to download the data
    from a specific site. Several errors are handled accordingly.
    """
    url = baseurl + subreddit + '.json'

    while True:
        try:
            r = requests.get(url,  headers={'User-Agent': 'Wallscraper Script by yhindy'})
            data = r.json()
            if r.ok:
                return data.get('data')
            elif data == None:
            	print('Hmm... something seems to have gone wrong, trying again...')
            elif data['error'] == 429:
                print('Too many requests, need to wait ...')
            time.sleep(10)
            query(subreddit)
        except requests.exceptions.ConnectionError:
            print ("requests ConnectionError, please make sure you are connected to the internet")
            break

def over500(subredditdata):
    """
    This function returns the number of posts that have over 500 votes
    in a specific subreddit
    """
    count = 0
    for child in subredditdata.get('children'):
        childdata = child.get('data')
        if childdata['score'] >= 500:
            count = count + 1

    return count