####################################
# This is tool to remove no-need data for the forum.
# It is for me only, Dont use it.
####################################
import json
import os
import time

from pymongo import MongoClient
from steem import Steem

####################################
# load config from json file
print('Reading config.json file')
with open('config.json') as json_config_file:
    config = json.load(json_config_file)
print(config)

# MongoDB
ns = os.environ['namespace'] if 'namespace' in os.environ else 'eostalk'
mongo = MongoClient(config['mongo_url'])
db = mongo[ns]

# Steem
nodes = config['steemd_nodes']
s = Steem(nodes)

# tags
matched_tags = ['eos', 'eosio', 'eos-project', 'eos-help', 'eos-support', 'eos-dev', 'eosdev', 'eos-dapp', 'eos-launchpad', 'eos-blockproducers', 'eos-meetups', 'eos-gov', 'eos-price', 'eos-disputes']

####################################

# check if comment contains:
#   - author: eosio
#   - tags: matched_tags
def is_filtered_post(post):
    try:
        if post['author'] == 'eosio':
            return True

        json_metadata = post['json_metadata']

        if isinstance(json_metadata, dict) and 'tags' in json_metadata and isinstance(json_metadata['tags'], list):
            if any(tag in matched_tags for tag in json_metadata['tags']):
                return True
        else:
            if isinstance(json_metadata, str) and len(json_metadata) > 0:
                metadata = json.loads(json_metadata)
                if 'tags' in metadata:
                    if any(tag in matched_tags for tag in metadata['tags']):
                        return True

    except ValueError as eValueError:
        print("ValueError {}".format(str(eValueError)))
    except TypeError as eTypeError:
        print("TypeError {}".format(str(eTypeError)))

    return False


def del_filtered_posts():
    counter = 0
    posts_count = db.posts.find({}).count()

    posts = db.posts.find({})
    for post in posts:
        if counter % 10 == 0:
            print('process {}/{}'.format(str(counter), str(posts_count)))
            time.sleep(0.1)

        if not is_filtered_post(post):
            print('found {}'.format(post['_id']))

            with open("/Volumes/RAMDisk/posts.txt", "a") as myfile:
                myfile.write(post['_id'] + '\n')

        counter = counter + 1


def process_del_posts():
    ids = []

    with open("/Volumes/RAMDisk/posts.txt", "r") as lines:
        for line in lines:
            print('.', end='', flush=True)
            id = line.strip()
            # print('processing: {}'.format(line))
            parts = id.split('/')
            author = parts[0].strip()
            permlink = parts[1].strip()
            # print('author={}, permlink={}'.format(author, permlink))
            # Fetch from the rpc
            post = s.get_content(author, permlink).copy()
            if not is_filtered_post(post):
                # print('found {}'.format(line))
                # db.posts.remove({'_id': id})
                ids.append(id)
                if len(ids) > 1:
                    db.posts.remove({"_id": {"$in": ids}})
                    ids = []
                    time.sleep(0.1)
                    print('found {}'.format(id))


def find_replies_to_delete():
    replies_items = db.replies.find({})
    for reply in replies_items:
        try:
            # print(reply)

            # check if the root_post is in posts collection or not, and delete it if not.
            root_post = reply['root_post']
            # print(root_post)

            found = db.posts.find({'_id': root_post}).count()
            if found == 0:
                print('Not found root_post={} for reply={}'.format(root_post, reply['_id']))

                with open("/Volumes/RAMDisk/replies.txt", "a") as myfile:
                    myfile.write(reply['_id'] + '\n')

        except KeyError as eKeyError:
            print("KeyError {}".format(str(eKeyError)))

            with open("/Volumes/RAMDisk/replies.txt", "a") as myfile:
                myfile.write(reply['_id'] + '\n')


def process_delete_replies():
    ids = []

    with open("/Volumes/RAMDisk/replies.txt", "r") as lines:
        for line in lines:
            print('.', end='', flush=True)
            id = line.strip()
            ids.append(id)
            if len(ids) > 100:
                db.replies.remove({"_id": {"$in": ids}})
                ids = []
                time.sleep(0.1)
                print('found {}'.format(id))


####################################
if __name__ == '__main__':
    print('del_filtered')
    process_delete_replies()
