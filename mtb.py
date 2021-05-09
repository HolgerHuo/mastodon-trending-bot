#!/usr/bin/env python3
import logging
import sys
import time
import json
import os
from pathlib import Path
import requests

base_path = os.path.dirname(__file__)

# Set logger configs
logger = logging.getLogger("Mastodon Trending Bot")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

time = time.asctime( time.localtime(time.time()) )

def read_file(path): 
    # Read file if it exists, and False on error.
    file = Path(path)
    if not file.is_file():
        return False
    try:
        file = open(path)
        data = file.read()
        file.close()
    except Exception as e:
        logger.critical("File reading error. Check if you have enough permissions to read the config.")
        logger.critical(e)
    return data

def config(key):  
    # Get config values from system environments and user-defined conf path (python3 mtb.py xxx.json) and the default path (config.json).
    if key in os.environ:
        return os.environ[key]
    
    conf = read_file(os.path.join(base_path, "config.json"))
    
    if len(sys.argv) > 1:
        conf = read_file(sys.argv[1])
              
    if not conf:
        logger.critical("Configuration not found. Exiting.")
        sys.exit()
        
    try:
        config = json.loads(conf)
    except Exception as e:
        logger.critical("Config file format error. Exiting.")
        logger.critical(e)
        sys.exit()
        
    if config.get(key):
        return config.get(key)
    else:
        return False
        
# Retreive all configurations 
if not config("MTB_APP_NAME") or not config("MTB_SOURCE_INSTANCE") or not config("MTB_DEST_INSTANCE") or not config("MTB_APP_SECURE_TOKEN") or not config("MTB_STATUS_VISIBILITY"):
    logger.critical("Config file incomplete. Exiting.")
    sys.exit()
app_name = config("MTB_APP_NAME")
mastodon_source_url = config("MTB_SOURCE_INSTANCE")
mastodon_dest_url = config("MTB_DEST_INSTANCE")
mastodon_dest_token = config("MTB_APP_SECURE_TOKEN")
tag_blacklist_path = config("MTB_BLACKLIST_PATH")
status_body = config("MTB_STATUS_BODY")
status_visibility = config("MTB_STATUS_VISIBILITY")
no_trends_status = config("MTB_NO_TRENDS_STATUS")

def construct_status():
    # Constructing status body 
    
    data = requests.get(mastodon_source_url+'/api/v1/trends.json').text

    if data is None:
        logger.critical(
            f"Could not retrieve trending info. Please make sure the instance URL ({mastodon_source_url}) is correct."
        )
        sys.exit()
        
    tags = json.loads(data)
             
    if status_body:
        post = status_body
    else:
        post = ""
        
    blacklist = []
    if tag_blacklist_path:
        blacklist_raw = read_file(os.path.join(base_path, tag_blacklist_path))
        if blacklist_raw:
            for line in blacklist_raw.splitlines():
                blacklist.append(line)

    tag_list = ''
    if tags:
        for tag in tags:
            if not tag["name"] in blacklist:
                # Check if exists in blacklist
                tag_list += '#' + tag["name"] + '\n'
                
    if tag_list:
        post = post + tag_list
        return post
    else:
        if no_trends_status:
            post = no_trends_status
            logger.info(
                f"No tags trending."
            )
            return post
        else:
            logger.info(
                    f"No tags trending. Exiting now."
            )
            sys.exit()
   

def toot(post):
    # Toot the toot!
    headers = {}
    headers["Authorization"] = f"Bearer {mastodon_dest_token}"
    data = {}
    data["status"] = post
    data["visibility"] = status_visibility

    response = requests.post(
        url=f"{mastodon_dest_url}/api/v1/statuses", json=data, headers=headers
    )

    if response.status_code == 200:
        logger.info(
            f"Tooted successfully at {time}."
        )
        logger.debug(f"Toot response: {response.text}")
        return True

    else:
        logger.error(
            f"Could not toot to {mastodon_dest_url}."
        )
        logger.error(f"Toot response: {response.text}")
        return False

# Go!
toot(construct_status().rstrip())