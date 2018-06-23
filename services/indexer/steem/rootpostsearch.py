####################################
# Porting rootpostsearch java version to python.
# WIP, dont use it!
####################################
import json
import inspect
import time
import sys
import os
import requests
from steem import Steem

####################################
# load config from json file
print('Reading config.json file')
with open('config.json') as json_config_file:
    config = json.load(json_config_file)
print(config)

# Steem
nodes = config['steemd_nodes']
s = Steem(nodes)

rps_store = {}

# find the comment, lookup from local store (rps_store) first, if not found then lookup remote
# comment_id = author/permlink
def rps_find_comment(comment_id):
    if rps_store.has_key(comment_id):
        return rps_store[comment_id]
    else:
        parts = comment_id.split('/')
        author = parts[0].strip()
        permlink = parts[1].strip()
        comment = s.get_content(author, permlink).copy()
        # Ensure a post was returned
        # if comment['author'] != '':




# comment_url = author/permlink
# def rps_find_root_post(comment_url):
    # if






def test_lookup():
    # with open('config.json') as json_config_file:
    #     config = json.load(json_config_file)
    # print(config['user'])

    # test_url = '\/life\/@intelliguy\/memes-are-great-when-used-sparingly-non-stop-memes-on-everything-irritates-me-am-i-the-only-one#@bartcardi\/re-intelliguy-re-bartcardi-re-intelliguy-memes-are-great-when-used-sparingly-non-stop-memes-on-everything-irritates-me-am-i-the-only-one-20180130t193540836z'
    # url = test_url.split('#')[0]
    # parts = url.split('/')
    # parent_id = parts[2].replace('@', '') + '/' + parts[3]
    # parent_id = parent_id.replace('\/', '/')
    # print(parent_id)


    data_comment = {
        'parent_author':'inuke',
        'parent_permlink':'tirangaa-1993-movie-review-26jan-republic-day-special',
        'author':'ivrmakers',
        'permlink':'re-inuke-tirangaa-1993-movie-review-26jan-republic-day-special-20180128t090400226z',
        'title':'',
        'body':'epic movie.. jaaanii',
        'json_metadata':'{"tags":["film"],"app":"steemit/0.1"}',
        'height':19369349,
        'timestamp':'2018-01-28T09:04:06',
        'txid':'394d79a1333ae940877773857ff9c710a8bd94c1'
    }

    response = requests.post('http://localhost:8080/api/lookup/filter/comment', data=json.dumps(data_comment), headers={'Content-type': 'application/json'})
    print(response.json()['data'])


if __name__ == '__main__':
    print('rootpostsearch')


